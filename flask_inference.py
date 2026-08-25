from flask import Flask, render_template, request, session, jsonify
import re
import json
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
import cvzone
from sort import *
import ast
from car_parking_coordinate_data import car_park_coordinate
app = Flask(__name__)

CORS(app)
app.secret_key = "a"
# JSON file to store user data
USER_DATA_FILE = "users.json"
# Path to store the JSON file
JSON_FILE = "contact_data.json"

# Function to load user data from the JSON file
def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save user data to the JSON file
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.route("/", methods=["GET", "POST"])
def project():
    return render_template("index.html")

@app.route("/hero")
def home():
    return render_template("index.html")

@app.route("/model")
def model():
    return render_template("model.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Create a new entry
    contact_entry = {"name": name, "email": email, "message": message}

    # Read existing data from JSON file
    try:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Append new entry to the data
    data.append(contact_entry)

    # Write updated data back to JSON file
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

    return jsonify({"status": "success", "message": "Contact details saved!"}), 200

@app.route("/reg", methods=["POST", "GET"])
def signup():
    msg = ""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Load user data
        users = load_users()

        # Check if the user already exists
        if email in users:
            return render_template("login.html", error=True)
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address"
        else:
            # Add new user
            users[email] = {"name": name, "password": password}
            save_users(users)
            msg = "Account created successfully"
    return render_template("login.html", msg=msg)

@app.route("/log", methods=["POST", "GET"])
def login1():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Load user data
        users = load_users()

        # Validate user credentials
        user = users.get(email)
        if user and user["password"] == password:
            session["Loggedin"] = True
            session["id"] = email
            session["email"] = email
            return render_template("model.html")
        else:
            msg = "Incorrect Email / Password"
            return render_template("login.html", msg=msg)
    else:
        return render_template("login.html")
    

@app.route("/predict", methods=["POST"])
def predict():
    if 'video_file' not in request.files:
        return jsonify({"error": "Video file and polygon file are required"}), 400

    # Retrieve video file
    video_file = request.files['video_file']
    video_path = f"Media/{video_file.filename}"
    video_file.save(video_path)
    print("video_path:", video_path)

    cap = cv2.VideoCapture(video_path)
    
    # Retrieve polygon option
    polygon_option = request.form.get('polygon_option')
    if not polygon_option:
        return jsonify({"error": "Polygon option is required"}), 400

    print("Selected Polygon Option:", polygon_option)

    # Initialize SORT tracker
    tracker = Sort(max_age=30)

    # Set of IDs for occupied parking spaces
    occupied_spaces = set()

    # Load class names
    classnames = []
    with open('classes.txt', 'r') as f:
        classnames = f.read().splitlines()
    model = YOLO('yolov11n_visdrone_model.pt')
    parking_polygons=car_park_coordinate(polygon_option)

    def is_parking_space_occupied(box_mid, parking_polygons):
        """Check if a detected vehicle overlaps with any parking space polygon."""
        for idx, polygon in enumerate(parking_polygons):
            if cv2.pointPolygonTest(polygon, box_mid, False) >= 0:
                return idx  # Return the index of the occupied parking space
        return None


    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = np.empty((0, 5))
        results = model(frame, stream=1)

        # Extract bounding boxes for "car" and "truck" classes
        for info in results:
            boxes = info.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                classindex = box.cls[0].item() 
                object_detected = classnames[int(classindex)]

                # Detect only cars or trucks with high confidence
                if object_detected == 'car':
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    new_detections = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, new_detections))

        # Update tracker
        track_result = tracker.update(detections)

        # Draw the parking spaces on the frame
        for idx, polygon in enumerate(parking_polygons):
            print(polygon)
            color = (0, 255, 0) if idx not in occupied_spaces else (0, 0, 255)
            cv2.polylines(frame, [polygon], isClosed=True, color=color, thickness=2)

        # Reset occupied spaces for this frame
        occupied_spaces.clear()

        # Process each tracked object
        for result in track_result:
            x1, y1, x2, y2, obj_id = map(int, result)

            # Calculate mid-point of the current bounding box
            box_mid = ((x1 + x2) // 2, (y1 + y2) // 2)

            # Check if the vehicle overlaps with any parking space
            occupied_space_idx = is_parking_space_occupied(box_mid, parking_polygons)
            if occupied_space_idx is not None:
                occupied_spaces.add(occupied_space_idx)

            # Draw bounding box and object ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cvzone.putTextRect(frame, f'ID: {obj_id}', [x1 + 5, y1 - 10], thickness=1, scale=1.2)

        # Display occupancy count and available spaces
        total_spaces = len(parking_polygons)
        occupied_count = len(occupied_spaces)
        available_count = total_spaces - occupied_count

        cvzone.putTextRect(frame, f'Total Spaces = {total_spaces}', [20, 40], thickness=2, scale=1.5, border=2)
        cvzone.putTextRect(frame, f'Occupied = {occupied_count}', [20, 80], thickness=2, scale=1.5, border=2)
        cvzone.putTextRect(frame, f'Available = {available_count}', [20, 120], thickness=2, scale=1.5, border=2)

        # Show the frame
        cv2.imshow('Smart Parking Occupancy', cv2.resize(frame, (1020, 500)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

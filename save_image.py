#1.SAVE FRAME GIVEN INTERNVAL TIME
import cv2
# Open the video file
video_path = 'Media/carpark_1.mp4'  # Replace with your video file path
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()
count = 0
# Read frames in a loop
while cap.isOpened():
    ret, frame = cap.read()  # Capture frame-by-frame
    if not ret:
        break  # Break the loop if there are no more frames

    # Process the frame (for example, display it)

    if count % 5 == 0:
        cv2.imwrite(f"save_image/sample_img_{count}.png",frame)

    cv2.imshow('Frame', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    count = count+5

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

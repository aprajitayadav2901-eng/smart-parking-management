# 🚗 GoPark – AI-Based Vehicle Parking Management System

GoPark is an AI-based vehicle parking management system developed using
Python, YOLO, OpenCV, Flask, and Computer Vision.

The system detects and monitors vehicles from video input and provides
automated vehicle tracking and parking monitoring capabilities.

---

## 🎥 Project Demo

Watch the GoPark system in action:

👉 [▶️ Watch GoPark Demo Video](https://drive.google.com/file/d/1FRjP86lc9vewTwoVIObPS6VAYWTxMMRE/view?usp=sharing)

> Make sure the Google Drive video sharing permission is set to
> **Anyone with the link → Viewer**.

---

## 🔗 Project Links

- 💻 [Source Code – GitHub](https://github.com/aprajitayadav2901-eng/GoPark-AI-Based-Vehicle-Parking-Management-System)
- 🎥 [Demo Video – Google Drive](https://drive.google.com/file/d/1FRjP86lc9vewTwoVIObPS6VAYWTxMMRE/view?usp=sharing)

---

## 📌 Project Overview

Parking areas often require continuous monitoring to identify vehicles
and understand parking occupancy.

GoPark uses Artificial Intelligence and Computer Vision to automate
vehicle detection and monitoring from video footage.

The system processes video input, detects vehicles using a YOLO model,
and tracks detected objects using the SORT tracking algorithm.

---

## 🎯 Objectives

- Detect vehicles automatically from video footage
- Track vehicles across video frames
- Monitor parking and vehicle movement
- Reduce manual monitoring
- Provide automated vehicle analysis
- Build a foundation for smart parking systems

---

## ✨ Features

- 🚗 Vehicle Detection
- 🎯 Object Tracking
- 🅿️ Parking Area Monitoring
- 📹 Video Processing
- 🤖 YOLO-based Object Detection
- 🔢 Vehicle Tracking IDs
- 🌐 Flask-based Application
- 📊 Automated Vehicle Monitoring
- ⚡ Real-Time Processing Support

---

## 🛠️ Tech Stack

### Programming Language

- Python

### Artificial Intelligence & Computer Vision

- YOLO
- OpenCV
- Computer Vision
- SORT Object Tracking

### Backend

- Flask

### Frontend

- HTML
- CSS
- JavaScript

### Data & Configuration

- JSON
- NumPy

### Tools

- Git
- GitHub
- Git LFS

---

## 🧠 Technologies Used

### YOLO

YOLO (You Only Look Once) is used for detecting objects in video
frames. The model identifies vehicles and provides their bounding boxes.

### OpenCV

OpenCV is used for:

- Reading video frames
- Image processing
- Drawing bounding boxes
- Video processing
- Displaying detection results

### SORT

SORT (Simple Online and Realtime Tracking) is used to track detected
vehicles across consecutive frames and assign tracking IDs.

### Flask

Flask is used to provide the application/backend interface for
running the vehicle monitoring functionality.

---

## 🔄 System Workflow

```text
             Input Video
                  │
                  ▼
          Video Frame Processing
                  │
                  ▼
            YOLO Detection
                  │
                  ▼
          Vehicle Identification
                  │
                  ▼
           SORT Object Tracking
                  │
                  ▼
          Tracking IDs Assigned
                  │
                  ▼
        Vehicle/Parking Monitoring
                  │
                  ▼
            Processed Output

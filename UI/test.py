import cv2
from ultralytics import YOLO
import os
# Load your trained YOLO model
model_path = "both_dataset.pt"  # Replace with the path to your trained model
model = YOLO(model_path)
# os.environ["XDG_SESSION_TYPE"] = "xcb"
# Open webcam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame from BGR to RGB (YOLO expects RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Use YOLO model to predict objects in the frame
    results = model.predict(frame_rgb, conf=0.5)  # You can set confidence threshold here

    # Draw bounding boxes, labels, and confidence scores on the frame
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get box coordinates
            conf = box.conf.item()  # Confidence of the detection
            class_id = int(box.cls.item())  # Class ID of the detected object
            class_name = model.names[class_id] if class_id < len(model.names) else "Unknown"

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label and confidence score
            label = f"{class_name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

    # Display the frame with detections
    cv2.imshow('YOLO Real-time Detection', frame)

    # Press 'q' to quit the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
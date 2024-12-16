from ultralytics import YOLO
import torch
import cv2
from PIL import Image

def inference(model: YOLO, input):
    results = model.predict(input)

    # Process results list
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        # print(f"Boxes: {boxes}")
        # print(f"Masks: {masks}")
        # print(f"Keypoints: {keypoints}")
        # print(f"Probs: {probs}")
        # print(f"Obb: {obb}")
        img = result.plot()  # display to screen


if __name__ == '__main__':
    model = YOLO('yolov8n.pt')
    input = 'dog_bike_car.jpg'
    input = cv2.imread(input)
    inference(model, input)
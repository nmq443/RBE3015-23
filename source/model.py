from ultralytics import YOLO
import torch
import cv2
from PIL import Image
from collections import Counter

class Model:
    def __init__(self, model: YOLO, device=None):
        if device is not None:
            self.device = device 
        else:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.model = model.to(device)
        self.total_objects = 0

    def count_objects(self, input):
        results = self.model.predict(input)
        confidence_threshold = 0.5


        # Process results list
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            valid_detections = [d for d in boxes if d.conf > confidence_threshold]
            total_objects = len(valid_detections)
            object_classes = [d.cls.item() for d in valid_detections]
            class_counts = Counter(object_classes)

            self.total_objects = total_objects

            # Print results
            print(f"Total objects detected: {total_objects}")
            print(f"Objects by class: {class_counts}")

        return results[0].plot()

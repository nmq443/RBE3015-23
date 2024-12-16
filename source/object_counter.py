from ultralytics import YOLO
import torch
import cv2
from PIL import Image
from collections import Counter

'''
cls_names = ['Button', 'Capacitor Jumper', 'Capacitor', 'Clock', 'Connector',
'Diode', 'EM', 'Electrolytic Capacitor', 'Ferrite Bead', 'IC', 'Inductor', 'Jumper', 'Led', 'Pads', 'Pins', 'Resistor Jumper', 'Resistor Network', 'Resistor', 'Switch', 'Test Point', 'Transistor', 'Unknown Unlabeled', 'iC', 'Crystal Oscillator']

cls_name = 'Transistor'
cls_idx = cls_names.index(cls_name)
'''

class ObjectCounter:
    def __init__(self, model: YOLO, device=None, confidence_threshold=0.2):
        if device is not None:
            self.device = device 
        else:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.model = model.to(device)
        self.confidence_threshold = confidence_threshold
        self.total_objects = 0
        
        self.class_names = self.model.names
        self.object_name = "Transistor"

    def count_objects(self, input):
        self.model.eval()
        results = self.model.predict(input)

        # Process results list
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            valid_detections = [d for d in boxes if d.conf >
                                self.confidence_threshold]
            total_objects = len(valid_detections)
            object_classes = [d.cls.item() for d in valid_detections]
            class_counts = Counter(object_classes)

            for cls, cls_count in class_counts.items():
                print(f"Class name: {self.class_names.get(cls, 'Unknown')}")

            self.total_objects = total_objects

            # Print results
            print(f"Total objects detected: {total_objects}")
            print(f"Objects by class: {class_counts}")

        return results[0].plot()

if __name__ == '__main__':
    model = YOLO('../weights/yolov8n.pt')
    cls_id = 2
    cls_names = model.names
    cls_name = cls_names.get(cls_id, "Unknown class")
    print(cls_name)

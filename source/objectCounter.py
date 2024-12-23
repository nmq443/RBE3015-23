from ultralytics import YOLO
import torch
from collections import Counter
import cv2
class ObjectCounter:
    def __init__(self, model: YOLO, cls_names, device=None, confidence_threshold=0.2):
        if device is not None:
            self.device = device
        else:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.model = model.to(self.device)
        self.confidence_threshold = confidence_threshold

        # Model's class names and filter only your desired classes
        self.model_class_names = self.model.names  # All classes from YOLO model
        self.cls_names = cls_names  # Desired classes to count
        self.cls_ids = [key for key, value in self.model_class_names.items() if value in self.cls_names]

    def count_objects(self, input):
        self.model.eval()
        results = self.model.predict(input, conf=self.confidence_threshold)

        # Initialize Counter for class counts
        overall_class_counts = Counter({name: 0 for name in self.cls_names})

        # Process results list
        for result in results:
            boxes = result.boxes  # Bounding boxes from the results
            valid_detections = [
                d for d in boxes if d.conf > self.confidence_threshold
            ]

            # Extract class IDs and count occurrences
            object_classes = [int(d.cls.item()) for d in valid_detections]
            class_counts = Counter(object_classes)

            # Filter only the desired classes and update counts
            for cls_id, count in class_counts.items():
                if cls_id in self.cls_ids:
                    class_name = self.model_class_names[cls_id]
                    overall_class_counts[class_name] += count

        # Print overall results
        print("\nOverall object counts:")
        for class_name, count in overall_class_counts.items():
            print(f"- {class_name}: {count}")

        return overall_class_counts  # Return the counts for further use

    def draw_bounding_boxes(self, input, output_path=None):
        self.model.eval()
        results = self.model.predict(input, conf=self.confidence_threshold)

        # Load image
        image = cv2.imread(input) if isinstance(input, str) else input

        for result in results:
            boxes = result.boxes  # Bounding boxes from the results
            for box in boxes:
                if box.conf > self.confidence_threshold:
                    cls_id = int(box.cls.item())
                    if cls_id in self.cls_ids:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                        label = f"{self.model_class_names[cls_id]} {box.conf.item():.2f}"
                        color = (0, 255, 0)  # Green for bounding boxes

                        # Draw rectangle
                        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

                        # Draw label
                        font_scale = 0.5
                        thickness = 1
                        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
                        cv2.rectangle(image, (x1, y1 - text_size[1] - 10), (x1 + text_size[0], y1), color, -1)
                        cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0),
                                    thickness)
        return image

if __name__ == '__main__':
    # Initialize model and class names
    model = YOLO('../weights/yolov8n.pt')
    cls_names = ['capacitor', 'connector', 'IC']  # Desired classes to count
    object_counter = ObjectCounter(model, cls_names)

    # Input can be an image, video file, or directory of images
    input_source = 'path_to_your_image_or_video'
    counts = object_counter.count_objects(input_source)

    # Display final counts
    print("\nFinal Object Counts:")
    for cls_name, count in counts.items():
        print(f"{cls_name}: {count}")

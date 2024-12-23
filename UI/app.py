import sys
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from app_handle import app_handle
from ultralytics import YOLO
from serial_arduino import *
model = YOLO('best.pt')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_ui = QMainWindow()
        self.main_handle = app_handle(self.main_ui)
        self.main_ui.show()
        self.set_logo()
        self.stream()
        self.image_number = 0
        self.control_arduino = SerialCommandSender()
        self.control_arduino.connect()
        self.main_handle.btn_capture_image.clicked.connect(self.capture_image)

    def stream(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            return

    def set_logo(self):
        logo_path = "logo/logo-2.png"
        pixmap = QPixmap(logo_path)

        pixmap = pixmap.scaled(self.main_handle.logo_uet.size(),
                               aspectRatioMode=Qt.KeepAspectRatio,
                               transformMode=Qt.SmoothTransformation)

        self.main_handle.logo_uet.setPixmap(pixmap)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Cannot read camera")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        widget_width = self.main_handle.image_stream.width()
        widget_height = self.main_handle.image_stream.height()

        results = model.predict(frame_rgb)

        if results:
            component_counts = {}

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls.item())
                    class_name = model.names[class_id] if class_id < len(model.names) else "Unknown"

                    if class_name in component_counts:
                        component_counts[class_name] += 1
                    else:
                        component_counts[class_name] = 1

            for component_name, count in component_counts.items():
                new_row_index = self.main_handle.compoment_table.rowCount()
                self.main_handle.compoment_table.insertRow(new_row_index)
                self.main_handle.compoment_table.setItem(new_row_index, 0, QTableWidgetItem(component_name))
                self.main_handle.compoment_table.setItem(new_row_index, 1, QTableWidgetItem(str(count)))

            total_components = sum(component_counts.values())
            self.main_handle.lbl_compoment_table.setText(f"Total components: {total_components}")

        resized_frame = cv2.resize(frame_rgb, (widget_width, widget_height))
        height, width, num_channels = resized_frame.shape
        bytes_per_line = num_channels * width

        qimage = QImage(resized_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.main_handle.image_stream.setPixmap(pixmap)

    def show_number_components(self):
        # Set self.main_handle.lbl_number.setText() with the number of components in the board
        pass

    def show_bounding_box_components(self):
        # Draw in the frame the bounding boxes of the components in the board
        pass

    def capture_image(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Cannot read camera")
            return

        # Ensure the directory exists before saving the image
        image_file = f'../image/capture_image{self.image_number}.jpg'
        cv2.imwrite(image_file, frame)
        print(f"Captured image saved as {image_file}")

        self.image_number += 1

    def error_board(self):
        self.control_arduino.send_command("00")

    def correct_board(self):
        self.control_arduino.send_command("01")

    def close_event(self, event):
        self.cap.release()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = App()
    sys.exit(app.exec_())

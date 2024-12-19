import sys
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from app_handle import app_handle
from ultralytics import YOLO

# model = YOLO('/home/hoang/xla/RBE3015-23/UI/best.pt')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_ui = QMainWindow()
        self.main_handle = app_handle(self.main_ui)
        self.main_ui.show()
        self.set_logo()
        self.stream()
        self.image_number = 0

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
        logo_path = "/home/hoang/xla/RBE3015-23/UI/logo/logo-2.png"
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

    def close_event(self, event):
        self.cap.release()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = App()
    sys.exit(app.exec_())

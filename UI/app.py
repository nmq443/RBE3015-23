import sys
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from app_handle import app_handle
from ultralytics import YOLO
from plc import SiemensPLC
from serial_communication import ArduinoSerial
# model = YOLO('/home/hoang/xla/RBE3015-23/UI/best.pt')
from source.objectCounter import ObjectCounter

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_ui = QMainWindow()
        self.main_handle = app_handle(self.main_ui)
        self.main_ui.show()
        self.set_logo()
        self.stream()
        self.image_number = 0
        #Plc control
        self.plc_control = SiemensPLC()
        self.plc_control.connect()
        #Arduino control
        self.arduino_control = ArduinoSerial()
        self.arduino_control.connect()

        self.model = YOLO('best.pt')
        self.class_name = ['capacitor', 'connector', 'IC']
        self.main_handle.btn_capture_image.clicked.connect(self.capture_image)
        self.start_read = 1
        self.start_write = 0

        self.object_counter = ObjectCounter(self.model, self.class_name)
        self.previous_value = 0
    def image_processing(self):
        current_value = self.plc_control.read_plc(3, 0 ,2)
        if self.previous_value  == 0 and current_value ==1:
            self.capture_image()
            self.plc_control.write_plc(3, 0, 0)
        self.previous_value = current_value

    def close_wiper(self):
        self.arduino_control.send_command("01")
    def open_wiper(self):
        self.arduino_control.send_command("00")
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
        # results = model.predict(frame_rgb)
        # if (self.plc_control.read_data(1, self.start_read, 2) == "01"):
        #     self.cap.

        resized_frame = cv2.resize(frame_rgb, (widget_width, widget_height))

        height, width, num_channels = resized_frame.shape
        bytes_per_line = num_channels * width

        qimage = QImage(resized_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        self.main_handle.image_stream.setPixmap(pixmap)



    def capture_image(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Cannot read camera")
            return

        # Ensure the directory exists before saving the image
        image_files = "D:/XLA/final/RBE3015-23/UI/image/"
        image_file = f'./image/capture_image/capture_image_{self.image_number}.jpg'
        cv2.imwrite(image_file, frame)
        print(f"Captured image saved as {image_file}")
        number_compoments = self.object_counter.count_objects(frame)
        self.update_component_table(self.image_number, number_compoments)
        print(number_compoments)
        if number_compoments['IC'] < 2 or number_compoments['capacitor'] < 5 or number_compoments['connector'] < 10:
            # self.close_wiper()
            self.main_handle.lbl_check.setText("Đủ")
        else:
            self.main_handle.lbl_check.setText("Thiếu")
            # self.open_wiper()
        image_bbox = self.object_counter.draw_bounding_boxes(frame)
        cv2.imwrite(f'./image/output_image/output_image_{self.image_number}.jpg', image_bbox)
        self.image_number += 1

    def close_event(self, event):
        self.cap.release()
        self.plc_control.disconnect()
        self.arduino_control.close()
        event.accept()

    def update_component_table(self, image_number ,component_counts):
        """
        Updates the table widget with the component counts for the current image.
        :param image_number: The order of the image being processed.
        :param component_counts: A dictionary containing component counts.
        """
        # Add a new row for the current image
        current_row = self.main_handle.compoment_table.rowCount()
        self.main_handle.compoment_table.insertRow(current_row)

        # Set the order of the image in the first column
        self.main_handle.compoment_table.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(image_number)))

        # Set the counts for each component in the respective columns
        component_columns = {
            'IC': 1,  # Column for IC
            'capacitor': 2,  # Column for capacitor
            'connector': 3  # Column for connector
        }

        for component, col_index in component_columns.items():
            count = component_counts.get(component, 0)
            self.main_handle.compoment_table.setItem(current_row, col_index, QtWidgets.QTableWidgetItem(str(count)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = App()
    sys.exit(app.exec_())

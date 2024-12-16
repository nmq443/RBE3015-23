import sys
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from appHandle import appHandle

class APP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainUi = QMainWindow()
        self.mainHandle = appHandle(self.mainUi)
        self.mainUi.show()

        self.stream()

    def stream(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            return

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Cannot read camera")
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = frame.shape
        bytesPerLine = width
        qimage = QImage(frame.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)
        self.mainHandle.Image_stream.setPixmap(pixmap)

    def show_number_compoment(self):
        #set  self.mainHandle.lbl_number.setText() the number of the compoment in the board
        pass

    def show_bbox_compoment(self):
        # Draw in frame the bbox of the compoment in the board
        pass


    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = APP()
    sys.exit(app.exec_())

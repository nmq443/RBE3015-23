from PyQt5.QtWidgets import QMainWindow
import main_ui

class appHandle(main_ui.Ui_MainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(main_window)

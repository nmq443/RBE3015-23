# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1026, 763)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image_stream = QtWidgets.QLabel(self.centralwidget)
        self.image_stream.setGeometry(QtCore.QRect(60, 260, 421, 311))
        self.image_stream.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.image_stream.setObjectName("image_stream")
        self.lbl_name_app = QtWidgets.QLabel(self.centralwidget)
        self.lbl_name_app.setGeometry(QtCore.QRect(120, 80, 711, 81))
        self.lbl_name_app.setStyleSheet("background-color:rgb(186, 235, 171);\n"
"font: 57 20pt \"Ubuntu\";")
        self.lbl_name_app.setObjectName("lbl_name_app")
        self.lbl_camera = QtWidgets.QLabel(self.centralwidget)
        self.lbl_camera.setGeometry(QtCore.QRect(80, 200, 81, 41))
        self.lbl_camera.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"border-radius:  10px;")
        self.lbl_camera.setObjectName("lbl_camera")
        self.compoment_table = QtWidgets.QTableWidget(self.centralwidget)
        self.compoment_table.setGeometry(QtCore.QRect(520, 260, 501, 311))
        self.compoment_table.setObjectName("compoment_table")
        self.compoment_table.setColumnCount(4)
        self.compoment_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.compoment_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.compoment_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.compoment_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.compoment_table.setHorizontalHeaderItem(3, item)
        self.btn_capture_image = QtWidgets.QPushButton(self.centralwidget)
        self.btn_capture_image.setGeometry(QtCore.QRect(330, 610, 111, 41))
        self.btn_capture_image.setStyleSheet("background-color:rgb(249, 240, 107);")
        self.btn_capture_image.setObjectName("btn_capture_image")
        self.logo_uet = QtWidgets.QLabel(self.centralwidget)
        self.logo_uet.setGeometry(QtCore.QRect(850, 40, 131, 131))
        self.logo_uet.setStyleSheet("background-color:#fff;")
        self.logo_uet.setObjectName("logo_uet")
        self.lbl_check = QtWidgets.QLabel(self.centralwidget)
        self.lbl_check.setGeometry(QtCore.QRect(520, 200, 111, 41))
        self.lbl_check.setStyleSheet("background-color: rgb(170, 200, 189);\n"
"border-radius:10px;")
        self.lbl_check.setText("")
        self.lbl_check.setObjectName("lbl_check")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.image_stream.setText(_translate("MainWindow", "Image stream"))
        self.lbl_name_app.setText(_translate("MainWindow", "App phát hiện số lượng linh kiện trên bảng mạch"))
        self.lbl_camera.setText(_translate("MainWindow", "Camera"))
        item = self.compoment_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "STT"))
        item = self.compoment_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "conector"))
        item = self.compoment_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "capacitor"))
        item = self.compoment_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "IC"))
        self.btn_capture_image.setText(_translate("MainWindow", "Capture Image"))
        self.logo_uet.setText(_translate("MainWindow", "Logo Uet"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

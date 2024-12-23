from plc import SiemensPLC
from UI.serial_communication import ArduinoSerial

class UI():
    def __init__(self):
        # arduino ------------------------------------------------
        self.control = ArduinoSerial()
        self.control.connect()
        # self.control.send_command("00")
        #arduino -------------------------------------------------
        # Cài đặt thông số kết nối PLC, lưu ý IP máy tính để 192.168.0.x
        plc_ip = "192.168.0.1"  # Địa chỉ IP của PLC
        rack = 0
        slot = 1
        db_number = 1  # Số DB (Data Block)
        start = 0      # Offset bắt đầu
        size = 2       # Kích thước dữ liệu (INT = 2 byte)
        self.controlPLC = SiemensPLC(plc_ip, rack, slot)
        self.controlPLC.connect()
        
        self.controlPLC.write_data(3,0,0)           # đưa giá trị phản hồi từ plc tại vị trí (db3 0 2) về 0
        self.previous_value = 0

    # hàm xử lý ảnh được thực hiện khi có giá trị data (db3 0 2) từ 0 lên 1
    def startXla(self):
    # Đọc giá trị hiện tại từ PLC
        current_value = self.controlPLC.read_data(3, 0, 2)
    
    # Kiểm tra nếu giá trị thay đổi từ 0 lên 1
        if self.previous_value == 0 and current_value == 1:
            # Thực hiện các lệnh khi có sự thay đổi
            self.controlPLC.write_data(3, 0, 0)
            self.capture_image()
    # Cập nhật trạng thái trước đó
        self.previous_value = current_value

    # hàm gửi dữ liệu đến arduino 00: ko gạt, 01: gạt
    def send00(self):
        self.control.send_command("00")
    def send01(self):
        self.control.send_command("01")  
    
    # khi write vào vị trí (db1, 0, "01") thì băng tải tiếp tục chạy
    def writePLC(self):
        data = "01"
        self.controlPLC.write_data(1,0,data)
    



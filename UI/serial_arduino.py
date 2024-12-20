import serial

class SerialCommandSender:
    def __init__(self, port="COM5", baudrate=9600, timeout=1):
        """
        Initialize the serial connection.
        :param port: The COM port to use (default: COM5).
        :param baudrate: The baud rate for communication (default: 9600).
        :param timeout: Read timeout in seconds (default: 1).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def connect(self):
        """Establish the serial connection."""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
            )
            if self.serial_connection.is_open:
                print(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")

    def send_command(self, command):
        """
        Send a command over the serial connection.
        :param command: The command string to send.
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                # Ensure the command ends with a newline for proper parsing
                if not command.endswith("\n"):
                    command += "\n"
                self.serial_connection.write(command.encode('utf-8'))
                print(f"Command sent: {command.strip()}")
            except Exception as e:
                print(f"Error sending command: {e}")
        else:
            print("Serial connection is not open.")

    def disconnect(self):
        """Close the serial connection."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Disconnected from {self.port}.")
        else:
            print("No connection to close.")



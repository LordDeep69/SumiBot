import serial
import time

class SerialCommunication:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Tiempo para establecer la conexión

    def send_message(self, message):
        self.serial_connection.write(message.encode('utf-8'))

    def receive_message(self):
        if self.serial_connection.in_waiting > 0:
            message = self.serial_connection.readline().decode('utf-8').strip()
            return message
        return None

    def close_connection(self):
        self.serial_connection.close()

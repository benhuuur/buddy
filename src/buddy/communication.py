# class ArduinoComm:
#     def __init__(self, port="/dev/ttyACM0", baudrate=9600):
#         self.ser = serial.Serial(port, baudrate, timeout=1)
#         time.sleep(2)  # aguarda Arduino inicializar

#     def send(self, message: str):
#         self.ser.write(f"{message}\n".encode('utf-8'))

#     def read(self):
#         if self.ser.in_waiting > 0:
#             return self.ser.readline().decode('utf-8').strip()
#         return None

#     def close(self):
#         self.ser.close()

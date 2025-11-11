import time


class Arduino:
    def __init__(self, port="COM3", baudrate=9600):
        # self.serial = serial.Serial(port, baudrate, timeout=1)
        # time.sleep(2)
        pass

    def send(self, message: str):
        print(f"{message}\n".encode('utf-8'))
        # self.serial.write(f"{message}\n".encode('utf-8'))

    # def read(self):
    #     if self.serial.in_waiting > 0:
    #         return self.serial.readline().decode('utf-8').strip()
    #     return None

    # def close(self):
    #     self.serial.close()

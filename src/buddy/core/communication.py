import time
import serial

from abc import ABC, abstractmethod
from serial.tools import list_ports


class Microcontroller(ABC):
    @abstractmethod
    def send(self, message: str):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def read(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def close(self):
        raise NotImplementedError("Subclasses must implement this method")


class Arduino(Microcontroller):
    def __init__(self, port: str | None = None, baudrate: int = 9600, timeout: float = 1.0):
        if port is None:
            port = self.find()
            if not port:
                raise serial.SerialException(
                    "No Arduino device found on available ports.")

        try:
            self.serial = serial.Serial(port, baudrate, timeout=timeout)
            time.sleep(2)

        except serial.SerialException as e:
            raise RuntimeError(f"Failed to connect to Arduino: {e}")

    def find(self) -> str | None:
        ports = list_ports.comports()
        for port in ports:
            if "Arduino" in port.description or "CH340" in port.description:
                return port.device
        return None

    def send(self, message: str) -> None:
        if not self.serial.is_open:
            raise ConnectionError("Serial port not open.")

        self.serial.write(f"{message}\n".encode("utf-8"))

    def read(self) -> str | None:
        if not self.serial.is_open:
            raise ConnectionError("Serial port not open.")

        if self.serial.in_waiting > 0:
            line = self.serial.readline().decode("utf-8", errors="ignore").strip()
            return line

        return None

    def close(self) -> None:
        self.serial.close()

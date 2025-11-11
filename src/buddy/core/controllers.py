import time

from abc import ABC, abstractmethod


class Controller(ABC):
    def __init__(self, setpoint: float) -> None:
        self.setpoint = setpoint

    @abstractmethod
    def compute(self, measurement):
        raise NotImplementedError(
            "Subclasses must implement the compute() method.")


class PID(Controller):
    def __init__(self, kp: float, ki: float, kd: float, setpoint=0.5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.last = 0
        self.tic = time.perf_counter()

    def compute(self, measurement: float):
        error = self.setpoint - measurement
        dt = time.perf_counter() - self.tic
        self.integral += error * dt
        derivative = (error - self.last) / dt
        self.last = error
        self.tic = time.perf_counter()
        return self.kp*error + self.ki*self.integral + self.kd*derivative

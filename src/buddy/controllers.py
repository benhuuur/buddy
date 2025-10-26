class PID:
    def __init__(self, kp, ki, kd, setpoint=0.5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.last = 0
        

    def update(self, measurement, dt=0.05):
        error = self.setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.last) / dt
        self.last = error
        return self.kp*error + self.ki*self.integral + self.kd*derivative

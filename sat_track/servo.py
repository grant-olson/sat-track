from time import sleep

class Servo:
    def __init__(self,pin,min=500, max=2500):
        # import here so we don't error if we're running on non-raspberry pi
        import pigpio

        self.min = min
        self.max = max
        self.pin = pin
        self.pi = pigpio.pi()
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
        
    def set_angle(self, angle):
        angle = float(angle)
        ms = (self.max - self.min) / 180.0 * angle
        ms += self.min
        self.pi.set_servo_pulsewidth(self.pin, ms)

    def set_pulsewidth(self, ms):
        self.pi.set_servo_pulsewidth(self.pin, ms)



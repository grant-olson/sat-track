import pigpio
from time import sleep

servo1 = 17


servo2 = 18

class Servo:
    def __init__(self,pin,min=500, max=2500):
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
        
servo1 = Servo(17)
servo2 = Servo(18, max=2350)

def calibration_check():
    print("Calibration Check, 0/0")
    servo1.set_angle(0)
    servo2.set_angle(0)

    sleep(5)

    print("Rotating 180")

    servo1.set_angle(180)
    sleep(5)

    print("Elevating 180")
    servo2.set_angle(180)
    sleep(5)

def rotation_test(minutes):
    substeps = 1000
    sleep_time = (60.0 * minutes) / substeps

    print(sleep_time)


    print("Rotation test... %d minute forward" % minutes)

    for i in range(substeps+1):
        angle = 180.0 * i / substeps
#        print(angle)
        servo1.set_angle(angle)
        servo2.set_angle(angle)
        sleep(sleep_time)
        
    print("Rotation test... %d minute reverse" % minutes)
    for i in range(substeps+1):
        angle = 180.0 - (180.0 * i / substeps)
#        print(angle)
        servo1.set_angle(angle)
        servo2.set_angle(angle)
        sleep(sleep_time)




if __name__ == "__main__":
    try:
        calibration_check()
#        for i in range(1,6):
#            rotation_test(i)
    except:
#        GPIO.cleanup()
        raise
    

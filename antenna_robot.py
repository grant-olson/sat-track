from servo import Servo
from time import sleep

class AntennaRobot:
    def __init__(self, azimuth_pin, elevation_pin,
               azimuth_min=500, azimuth_max=2500,
               elevation_min=500, elevation_max=2500):
        self.azimuth_servo = Servo(azimuth_pin, azimuth_min, azimuth_max)
        self.elevation_servo = Servo(elevation_pin, elevation_min, elevation_max)
        self.dir = "forward"
        self.update(0,0)
        sleep(0.5)

    def update(self, azimuth, elevation):
        azimuth = 360 - float(azimuth)
        elevation = float(elevation)

        if azimuth < 0.0 or azimuth > 360.0:
            raise RuntimeError("Azimuth %s should be between 0-360" % azimuth)

        if elevation < 0.0 or elevation > 360.0:
            raise RuntimeError("Elevation %s should be between 0-360" % elevation)
        if azimuth > 180.0:
            azimuth -= 180
            elevation = 180 - elevation
            current_dir = "backward"
        else:
            current_dir = "forward"

        self.azimuth_servo.set_angle(azimuth)
        self.elevation_servo.set_angle(elevation)

        if current_dir != self.dir:
            self.dir = current_dir
            sleep(1)

if __name__ == "__main__":
    robot = AntennaRobot(17,18, elevation_max=2350)
    robot.update(0,0)

    print("Rotate Azimuth 0 elevation")
    for i in range(0,360):
        robot.update(i,0)
        sleep(0.05)
        
    print("Rotate Azimuth 30 elevation")
    for i in range(0,360):
        robot.update(i,30)
        sleep(0.05)
        
    print("Rotate Azimuth Reverse 80 elevation")
    for i in range(0,360):
        robot.update(360-i,80)
        sleep(0.05)
        

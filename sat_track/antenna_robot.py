from .servo import Servo
from time import sleep

class AntennaRobot:
    def __init__(self, azimuth_pin, elevation_pin,
               azimuth_min=500, azimuth_max=2500,
               elevation_min=500, elevation_max=2500):
        self.azimuth_servo = Servo(azimuth_pin, azimuth_min, azimuth_max)
        self.elevation_servo = Servo(elevation_pin, elevation_min, elevation_max)
        self.dir = "forward"
        self.update(0,0)
        self.elevation_offset = 0.0
        self.azimuth_offset = 0.0
        sleep(0.5)

    def update(self, azimuth, elevation):
        azimuth = 360 - float(azimuth)
        elevation = float(elevation)

        if azimuth < 0.0 or azimuth > 360.0:
            raise RuntimeError("Azimuth %s should be between 0-360" % azimuth)

        if elevation < 0.0 or elevation > 180.0:
            raise RuntimeError("Elevation %s should be between 0-180" % elevation)

        # Add offsets and fix if we over/underflow
        elevation += self.elevation_offset
        azimuth += self.azimuth_offset

        if elevation > 180.0:
            elevation -= 180.0
        elif elevation < 0.0:
            elevation += 180.0

        if azimuth > 360.0:
            azimuth -= 360.0
        elif azimuth < 0.0:
            azimuth += 360

        # Flip control since servos only go 180 degrees
            
        if azimuth > 180.0:
            azimuth -= 180
            elevation = 180 - elevation
            current_dir = "backward"
        else:
            current_dir = "forward"

        self.azimuth_servo.set_angle(azimuth)
        self.elevation_servo.set_angle(elevation)

        # pause a bit if we need to flip controls
        if current_dir != self.dir:
            self.dir = current_dir
            sleep(1)


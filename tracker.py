from satellite_directory import Home, todays_directory
from antenna_robot import AntennaRobot
from time import sleep
import sys

class Tracker:
    def __init__(self, robot, home):
        self.robot = robot
        self.home = home
        self.directory = todays_directory()

    def decimal_angle(self,degrees,minutes,seconds):
        return float(degrees) + (float(minutes) / 60) + (float(seconds) / 3600)

    def track(self, satellite):

        next_pass = self.directory.get_next_pass(satellite, self.home)
        if not next_pass['success']:
            print("No passes in next 24 hours. Won't Track.")
            return

        print("Next Pass starts at %s." % next_pass['start'])
        if 'finish' in next_pass:
            pass_time = next_pass['finish'] - next_pass['start']
            pass_minutes = pass_time.seconds / 60
            pass_seconds = pass_time.seconds % 60
            print("Pass length %d m %d s" % (pass_minutes, pass_seconds))
            
        print("===")
            
        started_pass = False
        last_az = 0
        last_el = 0
    
        while True:
            el, az, distance = self.directory.get_current_azimuth_and_elevation(satellite, home)
            az_d, az_m, az_s = az.dms()
            decimal_az = self.decimal_angle(az_d, az_m, az_s)

            if decimal_az < 0:
                decimal_az += 360
        
            el_d, el_m, el_s = el.dms()
            decimal_el = self.decimal_angle(el_d, el_m, el_s)
    
            if decimal_el < 0:
                print("BELOW HORIZON %f %f" % (decimal_az, decimal_el))
                robot.update(decimal_az, 0.0)
                if started_pass:
                    print("FINISHED TRACKING")
                    return
                else:
                    sleep(30)

            else:
                robot.update(decimal_az, decimal_el)
                if (last_az != az_d) or (last_el != el_d):
                    print("TRACKING %0.2f %0.2f" % (decimal_az, decimal_el))
                    last_az = az_d
                    last_el = el_d
                    sleep(0.05)
                    started_pass = True
        

if __name__ == "__main__":
    home = Home("EN90xj")
    robot = AntennaRobot(4,22, elevation_max=2350, elevation_min=600)
    tracker = Tracker(robot, home)

    
    tracker.track(sys.argv[1])

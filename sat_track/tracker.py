from .satellite_directory import Home, todays_directory
from .antenna_robot import AntennaRobot
from .display import CursesDisplay
from time import sleep
import sys

class Tracker:
    def __init__(self, robot, home):
        self.robot = robot
        self.home = home
        self.directory = todays_directory()
        self.display = CursesDisplay()
#        self.display.set_header(3, "Pass Start")
        for header, row in {"Pass Start": 3, "Pass Finish": 4, "Current Tracking": 6}.items():
            self.display.set_header(row, header)

    def __del__(self):
        self.display = None
            
    def decimal_angle(self,degrees,minutes,seconds):
        return float(degrees) + (float(minutes) / 60) + (float(seconds) / 3600)

    def track(self, satellite):

        next_passes = self.directory.get_next_passes(satellite, self.home)
        if len(next_passes) < 1:
            print("No passes in next 24 hours. Won't Track.")
            return

        next_pass = next_passes[0]
        
        self.display.update_status("Pass Start", "Next Pass starts at %s." % next_pass['start'])
        if 'finish' in next_pass:
            pass_time = next_pass['finish'] - next_pass['start']
            pass_minutes = pass_time.seconds / 60
            pass_seconds = pass_time.seconds % 60
            self.display.update_status("Pass Finish", "Pass length %d m %d s" % (pass_minutes, pass_seconds))
            
        started_pass = False
        last_az = 0
        last_el = 0
    
        while True:
            ch = self.display.window.getch()
            if ch != -1:
                ch = chr(ch)
                if ch == 'w':
                    self.robot.elevation_offset += 1
                elif ch == 's':
                    self.robot.elevation_offset -= 1
                elif ch == "a":
                    self.robot.azimuth_offset -= 1
                elif ch == 'd':
                    self.robot.azimuth_offset += 1

            el, az, distance = self.directory.get_current_azimuth_and_elevation(satellite, self.home)
            az_d, az_m, az_s = az.dms()
            decimal_az = self.decimal_angle(az_d, az_m, az_s)

            if decimal_az < 0:
                decimal_az += 360
        
            el_d, el_m, el_s = el.dms()
            decimal_el = self.decimal_angle(el_d, el_m, el_s)
    
            if decimal_el < 0:
                self.display.update_status("Current Tracking", ("BELOW HORIZON %f %f %d %d" % (decimal_az, decimal_el, self.robot.azimuth_offset, self.robot.elevation_offset)))
                self.robot.update(decimal_az, 0.0)
                if started_pass:
                    print("FINISHED TRACKING")
                    return
                else:
                    sleep(30)

            else:
                self.robot.update(decimal_az, decimal_el)
                if (last_az != az_d) or (last_el != el_d):
                    self.display.update_status("Current Tracking","TRACKING %0.2f %0.2f %d %d" % (decimal_az, decimal_el, self.robot.azimuth_offset, self.robot.elevation_offset))
                    last_az = az_d
                    last_el = el_d
                    sleep(0.05)
                    started_pass = True
        


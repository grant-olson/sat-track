from servo import Servo

import sys

cmd, az, el = sys.argv

az_servo = Servo(4)
el_servo = Servo(22)

az_servo.set_pulsewidth(az)
el_servo.set_pulsewidth(el)

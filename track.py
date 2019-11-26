from satellite_directory import Home, SatelliteDirectory
from time import sleep

home = Home("EN90xj")

directory = SatelliteDirectory()
directory.add_keplerian("NOAA 18",
                    "1 28654U 05018A   19329.58873065  .00000093  00000-0  75226-4 0  9993",
                    "2 28654  99.0757  18.7938 0015197  88.8661 271.4251 14.12469460748097")

az_el = directory.get_current_azimuth_and_elevation("NOAA 18", home)

def decimal_angle(degrees,minutes,seconds):
    return float(degrees) + (float(minutes) / 60) + (float(seconds) / 3600)

def track_it(satellite, home):
    started_pass = False

    while True:
        el, az, distance = directory.get_current_azimuth_and_elevation(satellite, home)
        az_d, az_m, az_s = az.dms()
        decimal_az = decimal_angle(az_d, az_m, az_s)

        el_d, el_m, el_s = el.dms()
        decimal_el = decimal_angle(el_d, el_m, el_s)
    
        if decimal_el < 0:
            print("BELOW HORIZON %d" % decimal_el)
            if started_pass:
                print("FINISHED TRACKING")
                return
            else:
                sleep(30)

        else:
            print("TRACKING")
            sleep(0.05)
            started_pass = True
        

if __name__ == "__main__":
    track_it("NOAA 18", home)

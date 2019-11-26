import maidenhead
from skyfield.api import load, Topos, EarthSatellite, Timescale, utc
from datetime import datetime, timedelta

ts = load.timescale()

class Home:
    def __init__(self, grid_square):
        self.grid_square = grid_square
        self.latitude, self.longitude = maidenhead.toLoc(grid_square)
        self.topo = Topos(self.latitude, self.longitude)
        
class SatelliteDirectory:
    def __init__(self):
        self.satellites = {}

    def add_keplerian(self,name,k1,k2):
        s = EarthSatellite(k1,k2,name=name)
        self.satellites[name] = s

    def get_diff(self, name, home):
        s = self.satellites[name]
        diff = s - home.topo
        return diff

    def get_azimuth_and_elevation(self, name, home, time):
        diff = self.get_diff(name, home)
        return diff.at(time).altaz()

    def get_current_azimuth_and_elevation(self, name, home):
        return self.get_azimuth_and_elevation(name, home, ts.now())

    def get_next_pass(self, name, home):
        """
        Get next pass with a limit of 24 hours
        """
        now = datetime.now(utc)
        found_pass = False

        results = {}
        
        for i in range(0,60*24):
            next_time = now + timedelta(0,60*i) # add appropriate number of seconds
            next_timescale = ts.utc(next_time)
            el, az, distance = self.get_azimuth_and_elevation(name, home, next_timescale)

            d, m, s = el.dms()
            
            if found_pass:
                if d < 0:
                    results["finish"] = next_time
                    break
            else:
                if d >= 0:
                    results["start"] = next_time
                    found_pass = True

        results["success"] = found_pass
        return results
                    
if __name__ == "__main__":
    
    home = Home("EN90xj")

    directory = SatelliteDirectory()
    directory.add_keplerian("NOAA 18",
                        "1 28654U 05018A   19329.58873065  .00000093  00000-0  75226-4 0  9993",
                        "2 28654  99.0757  18.7938 0015197  88.8661 271.4251 14.12469460748097")



    az_el = directory.get_current_azimuth_and_elevation("NOAA 18", home)

    print(az_el)


    print("NEXT PASS")
    next_pass = directory.get_next_pass("NOAA 18", home)
    if next_pass['success']:
        if 'finish' in next_pass:
            print("Start: %s Finish: %s" % (next_pass['start'], next_pass['finish']))
        else:
            print("Start: %s Finish: AFTER 24 HOURS" % next_pass['start'])

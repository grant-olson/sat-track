import maidenhead
from skyfield.api import load, Topos, EarthSatellite, Timescale, utc
from datetime import datetime, timedelta
import sys

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

    def add_tle_url(self, url):
        sats = load.tle(url)
        self.satellites.update(sats)
        
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


def todays_directory():
    directory = SatelliteDirectory()

    urls = {"Amateur": "https://celestrak.com/NORAD/elements/amateur.txt",
            "NOAA Weather": "https://celestrak.com/NORAD/elements/noaa.txt",
            "GOES Weather": "https://www.celestrak.com/NORAD/elements/goes.txt"
    }

    for name, url in urls.items():
        print("Loading %s..." % name)
        directory.add_tle_url(url)

    return directory

if __name__ == "__main__":
    
    home = Home("EN90xj")

    directory = todays_directory()

    if len(sys.argv) > 1:
        
        satellites = sys.argv[1:]
        
    else:
        print("No satellite provided. Deafulting to NOAA 15")
        satellites = ["NOAA 15"]

    results = []
        
    for sat in satellites:

        az_el = directory.get_current_azimuth_and_elevation(sat, home)

        next_pass = directory.get_next_pass(sat, home)
        if next_pass['success']:
            if 'finish' in next_pass:
                results.append((sat, next_pass['start'], next_pass['finish']))
            else:
                results.append((sat, next_pass['start'], None))

results.sort(key=lambda tup: tup[1])

print("Current Time: %s\n" % datetime.now(utc))

biggest_name = 0
for result in results:
    name, start, finish = result
    name_length = len(name)
    if name_length > biggest_name:
        biggest_name = name_length
        
for result in results:
    name, start, finish = result

    start = start.strftime("%m-%d %H:%M")

    if finish is None:
        finish = "Unknown"
    else:
        finish = finish.strftime("%H:%M")
            
    
    format_string = "Satellite: %" + str(biggest_name) +"s Start: %s Finish: %s"
    print( format_string % (name, start, finish))

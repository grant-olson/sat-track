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

    def get_next_passes(self, name, home, window=24*60):
        """
        Get next passes with a default limit of 24 hours
        """
        now = datetime.now(utc)
        found_pass = False

        results = []
        next_pass = {}
    
        for i in range(0,window):
            next_time = now + timedelta(0,60*i) # add appropriate number of seconds
            next_timescale = ts.utc(next_time)
            el, az, distance = self.get_azimuth_and_elevation(name, home, next_timescale)

            d, m, s = el.dms()
            
            if "start" in next_pass:
                if d < 0:
                    next_pass["finish"] = next_time
                    next_pass["finish_azimuth"] = az.dms()[0]
                    results.append(next_pass)
                    next_pass = {}
                else:
                    if d > next_pass["max_elevation"]:
                        next_pass["max_elevation"] = d
            else:
                if d >= 0:
                    next_pass["name"] = name
                    next_pass["start"] = next_time
                    next_pass["start_azimuth"] = az.dms()[0]
                    next_pass["max_elevation"] = d

        if "start" in next_pass: # Pass that didn't finish
            next_pass["finish_azimuth"] = az.dms()[0]
            results.append(next_pass)
        return results

    def list_next_passes(self, home, satellites):
        results = []
        
        for sat in satellites:
            next_passes = self.get_next_passes(sat, home)
            if len(next_passes) > 0:
                results.extend(next_passes)
                
        results.sort(key=lambda d: d['start'])

        print("Current Time: %s\n" % datetime.now(utc))

        print("")

        print("+----------------------+-------+--------+-----+--------+----------+----------+")
        print("|       Satellite      | Start | Finish | Len | Max El | Start Az | Finish Az|")
        print("+----------------------+-------+--------+-----+--------+----------+----------+")
        for result in results:
            name = result['name']
            start = result['start']
            start_az = result['start_azimuth']
            max_el = result['max_elevation']
            finish_az = result['finish_azimuth']

            if 'finish' in result:
               finish = result['finish']
               length = (finish - start).seconds / 60
            
               
            else:
                finish = None
                length = -1

            start = start.strftime("%H:%M")

            if finish is None:
                finish = "?????"
            else:
                finish = finish.strftime("%H:%M")

    
            print( "| %20s | %s |  %s | %3d |    %3d |      %3d |       %3d|" % (name, start, finish, length, max_el, start_az, finish_az))
        print("+----------------------+-------+--------+-----+--------+----------+----------+")



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
        satellites = ["NOAA 15 [B]"]

    directory.list_next_passes(home, satellites)

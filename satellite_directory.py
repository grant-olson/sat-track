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
    
if __name__ == "__main__":
    
    home = Home("EN90xj")

    directory = SatelliteDirectory()
    directory.add_keplerian("NOAA 18",
                        "1 28654U 05018A   19329.58873065  .00000093  00000-0  75226-4 0  9993",
                        "2 28654  99.0757  18.7938 0015197  88.8661 271.4251 14.12469460748097")



    az_el = directory.get_current_azimuth_and_elevation("NOAA 18", home)

    print(az_el)


    # print("NEXT HOUR")
    # now = datetime.utcnow()
    # for i in range(0,60):
    #     next_time = now + timedelta(0,60*i)
    #     next_timescale = Timescale.utc(next_time)
    #     az_el = directory.get_azimuth_and_elevation("NOAA 18", home, next_timescale)
    #     print("%i %s" % (i, az_el))

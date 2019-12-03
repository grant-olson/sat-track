import os
import yaml

from .antenna_robot import AntennaRobot

class Config:
    def default_config(self):
        return {
            "robot":
                    {"azimuth": {"pin": 4}, "elevation": {"pin": 22}},
            "home": {"grid_square": "EN90xj"},
            "satellite": {
                "tles": {
                    "Amateur": "https://celestrak.com/NORAD/elements/amateur.txt",
                    "NOAA Weather": "https://celestrak.com/NORAD/elements/noaa.txt",
                    "GOES Weather": "https://www.celestrak.com/NORAD/elements/goes.txt",
                    "Iridium NEXT": "https://celestrak.com/NORAD/elements/iridium-NEXT.txt"
                    },
                "favorites": ["NOAA 15 [B]" "NOAA 18 [B]" "NOAA 19 [+]" "FOX-1D (AO-92)" "FOX-1B" "SAUDISAT 1C (SO-50)"]
                    }
                }
        
    def __init__(self, config_file):
        if not os.path.exists(config_file):
            f = open(config_file,"w")
            yaml.dump(self.default_config(), f)
            f.close()

        self.config = yaml.load(open(config_file))
        
    def grid_square(self):
        return self.config['home']['grid_square']

    def azimuth_pin(self):
        return self.config['robot']['azimuth']['pin']

    def azimuth_max(self):
        if 'max' in self.config['robot']['azimuth']:
            return self.config['robot']['azimuth']['max']
        else:
            return 2500
    
    def azimuth_min(self):
        if 'min' in self.config['robot']['azimuth']:
            return self.config['robot']['azimuth']['min']
        else:
            return 500
    
    def elevation_pin(self):
        return self.config['robot']['elevation']['pin']
    
    def elevation_max(self):
        if 'max' in self.config['robot']['elevation']:
            return self.config['robot']['elevation']['max']
        else:
            return 2500
    
    def elevation_min(self):
        if 'min' in self.config['robot']['elevation']:
            return self.config['robot']['elevation']['min']
        else:
            return 500

    def favorites(self):
        if 'satellite' not in self.config:
            return[]
        
        if 'favorites' in self.config['satellite']:
            return self.config['satellite']['favorites']
        else:
            return []

    def tles(self):
        if 'satellite' not in self.config:
            return {}
        
        if 'tles' in self.config['satellite']:
            return self.config['satellite']['tles']
        else:
            return {}
        
current_config = None

def load_config():
    global current_config
    if current_config is None:
        print("Loading config...")
        current_config = Config("./config.yaml")

def get_home():
    from .satellite_directory import Home
    load_config()
    return Home(current_config.grid_square())

def get_robot():
    load_config()
    return AntennaRobot(current_config.azimuth_pin(), current_config.elevation_pin(),
                            azimuth_min=current_config.azimuth_min(), azimuth_max=current_config.azimuth_max(),
                            elevation_min=current_config.elevation_min(), elevation_max=current_config.elevation_max())

def get_azimuth_pin():
    load_config()
    return current_config.azimuth_pin()

def get_elevation_pin():
    load_config()
    return current_config.elevation_pin()

def get_favorite_satellites():
    load_config()
    return current_config.favorites()
    
def get_satellite_tles():
    load_config()
    return current_config.tles()
    
__all__ = ["get_home", "get_robot", "get_azimuth_pin", "get_elevation_pin", "get_favorite_satellites", "get_satellite_tles"]

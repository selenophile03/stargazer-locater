import streamlit as st
from skyfield.api import load, wgs84, Star
from skyfield.data import hipparcos, iau
from config import COUNTRY_GEO_DB

class ConstellationLocator:
    @st.cache_resource
    def _load_data(_self):
        eph = load('de421.bsp')
        ts = load.timescale()
        constellation_at = iau.load_constellation_map()
        with load.open(hipparcos.URL) as f:
            star_dataframe = hipparcos.load_dataframe(f)
        return eph, ts, constellation_at, star_dataframe

    def __init__(self):
        self.eph, self.ts, self.constellation_at, self.star_dataframe = self._load_data()
        self.earth = self.eph['earth']
            
    def get_visible_constellations(self, country_name, observation_time=None):
        if country_name not in COUNTRY_GEO_DB:
            raise ValueError(f"Country '{country_name}' not found in configuration.")
            
        geo_data = COUNTRY_GEO_DB[country_name]
        observer_loc = self.earth + wgs84.latlon(geo_data['lat'], geo_data['lon'])
        
        t = self.ts.now() if observation_time is None else self.ts.from_datetime(observation_time)
        visible_constellations = {}
        bright_stars = self.star_dataframe[self.star_dataframe['magnitude'] <= 5.0]
        
        for hip_id, row in bright_stars.iterrows():
            star_obj = Star.from_dataframe(row)
            astrometric = observer_loc.at(t).observe(star_obj)
            alt, az, distance = astrometric.apparent().altaz()
            
            if alt.degrees > 0:
                const_abbreviation = self.constellation_at(astrometric)
                
                if const_abbreviation not in visible_constellations:
                    visible_constellations[const_abbreviation] = {
                        'highest_altitude': alt.degrees,
                        'sample_azimuth': az.degrees
                    }
                else:
                    if alt.degrees > visible_constellations[const_abbreviation]['highest_altitude']:
                        visible_constellations[const_abbreviation]['highest_altitude'] = alt.degrees
                        visible_constellations[const_abbreviation]['sample_azimuth'] = az.degrees
                        
        return visible_constellations, t

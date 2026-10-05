import streamlit as st
import pandas as pd
from locator import ConstellationLocator
from config import COUNTRY_GEO_DB

st.set_page_config(page_title="Stargazer Constellation Locator", layout="centered")

st.title("Stargazer Constellation Locator")
st.write("Track which constellations are currently visible above the horizon from your location.")

@st.cache_resource
def get_engine():
    return ConstellationLocator()

try:
    engine = get_engine()
    
    country_list = list(COUNTRY_GEO_DB.keys())
    target_country = st.selectbox("Select Country", country_list)
    
    if st.button("Find Visible Constellations"):
        with st.spinner("Calculating coordinates..."):
            results, exact_time = engine.get_visible_constellations(target_country)
            
            st.success(f"Calculation complete for {COUNTRY_GEO_DB[target_country]['city']}, {target_country}")
            st.write(f"Observation Time: {exact_time.utc_strftime()} UTC")
            
            sorted_constellations = sorted(results.items(), key=lambda x: x['highest_altitude'], reverse=True)
            
            table_data = []
            for code, metrics in sorted_constellations:
                table_data.append({
                    "Constellation": code,
                    "Altitude (Elevation)": f"{metrics['highest_altitude']:.2f}°",
                    "Azimuth (Direction)": f"{metrics['sample_azimuth']:.2f}°"
                })
                
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"Total visible constellations tracked: {len(sorted_constellations)}")
            
except Exception as e:
    st.error(f"Application error: {e}")

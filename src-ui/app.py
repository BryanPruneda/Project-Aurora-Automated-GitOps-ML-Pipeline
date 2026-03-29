import streamlit as st
import redis
import os

# Connect to Redis
r = redis.Redis(host='aurora-redis-service', port=6379, db=0, decode_responses=True)

st.set_page_config(page_title="Terra Texas", page_icon="🌵")
st.title("🌵 Project Terra: Texas Soil Monitor")

# Get live data from Database
soil_temp = r.get('texas_soil_temp')

if soil_temp:
    temp_val = float(soil_temp)
    st.metric(label="Current Fort Worth Soil Temp", value=f"{temp_val}°C")
    
    if temp_val > 15:
        st.success("☀️ Warm enough for spring planting!")
    else:
        st.warning("❄️ Soil is still a bit chilly.")
else:
    st.info("Waiting for data from the Texas Worker...")

st.divider()
st.write("Live Data sourced from Open-Meteo Satellite Feeds")

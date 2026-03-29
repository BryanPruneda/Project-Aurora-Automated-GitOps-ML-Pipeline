import streamlit as st
import redis
import pandas as pd

r = redis.Redis(host='aurora-redis-service', port=6379, db=0, decode_responses=True)

st.set_page_config(page_title="Terra Texas Pro", layout="wide")
st.title("🌵 Texas Soil Intelligence Dashboard")

col1, col2 = st.columns([1, 1])

with col1:
    soil_temp = r.get('texas_soil_temp')
    if soil_temp:
        st.metric("Fort Worth Soil Temp", f"{soil_temp}°C")
        # Visual Map
        df = pd.DataFrame({'lat': [32.7555], 'lon': [-97.3308]})
        st.map(df)

with col2:
    st.subheader("Regional Stats")
    if soil_temp and float(soil_temp) < 5:
        st.error("🚨 FREEZE WARNING: Protect your crops!")
    else:
        st.success("🍀 Conditions are stable.")
    
    st.info("Historical tracking active in PostgreSQL.")

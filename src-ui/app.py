import streamlit as st
import redis
import pandas as pd
import numpy as np
import json
import pydeck as pdk
import psycopg2
import pytz
from datetime import datetime

# 1. Setup & Connections
st.set_page_config(page_title="Aurora: Lone Star Edition", layout="wide")
r = redis.Redis(host='aurora-redis-service', port=6379, db=0, decode_responses=True)
texas_tz = pytz.timezone('US/Central')

def get_history():
    try:
        conn = psycopg2.connect(host="aurora-postgres-service", database="postgres", user="postgres", password="fortworth")
        # Get last 100 readings for the chart
        df = pd.read_sql("SELECT ts, temp, CONCAT(lat, ',', lon) as point_id FROM soil_history ORDER BY ts DESC LIMIT 100", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

# 2. Main UI
st.title("🤖 Project Aurora: The AI Oracle")

raw_grid = r.get('texas_grid_data')
if raw_grid:
    grid_df = pd.DataFrame(json.loads(raw_grid))
    st.sidebar.header("Command Center")
    all_cities = grid_df['id'].tolist()
    selected_names = st.sidebar.multiselect("Select Cities to Analyze:", all_cities, default=["Fort Worth"])

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Texas Intelligence Map")
        filtered_df = grid_df[grid_df['id'].isin(selected_names)]
        layer = pdk.Layer(
            "ScatterplotLayer", 
            filtered_df, 
            pickable=True, 
            get_position=["lon", "lat"],
            get_radius=15000, 
            get_fill_color="[255, 215, 0, 200]", 
            radius_min_pixels=8
        )
        st.pydeck_chart(pdk.Deck(
            layers=[layer], 
            initial_view_state=pdk.ViewState(latitude=31.0, longitude=-100.0, zoom=5),
            tooltip={"text": "{id}: {temp}°C"}
        ))
        
        # --- THE POSTGRES PORTION ---
        st.divider()
        st.subheader("📈 Historical Trends (Postgres)")
        hist_df = get_history()
        if not hist_df.empty:
            hist_df['ts'] = pd.to_datetime(hist_df['ts']).dt.tz_localize('UTC').dt.tz_convert(texas_tz)
            # Filter history to show only selected cities if data exists
            st.line_chart(hist_df.set_index('ts')['temp'])
        else:
            st.info("Waiting for Postgres to collect more history...")

    with col2:
        st.subheader("📰 AI Daily Briefing")
        if selected_names:
            now_texas = datetime.now(texas_tz)
            time_str = now_texas.strftime('%I:%M %p %Z')

            avg_temp = filtered_df['temp'].mean()
            coldest = filtered_df.loc[filtered_df['temp'].idxmin()]
            
            st.info(f"**Texas Report:** It is currently **{time_str}**. "
                    f"Average soil temp: {avg_temp:.1f}°C. "
                    f"Coldest Hub: **{coldest['id']}** ({coldest['temp']}°C).")
            
            st.divider()
            st.subheader("🔮 Oracle Forecast")
            for city in selected_names:
                city_temp = filtered_df[filtered_df['id'] == city]['temp'].values[0]
                # The 'Brain' logic
                pred = round(city_temp + (np.random.uniform(-0.5, 0.5)), 2)
                st.write(f"**{city}**: Now {city_temp}°C → **1hr: {pred}°C**")
        else:
            st.write("Select a city to begin analysis.")

else:
    st.warning("Booting Texas-wide satellite relay...")

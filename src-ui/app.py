import streamlit as st
import redis
import pandas as pd
import numpy as np
import json
import pydeck as pdk
import psycopg2
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. Setup & Connections
st.set_page_config(page_title="Project Aurora: Texas Soil Temperatures", layout="wide")
r = redis.Redis(host='aurora-redis-service', port=6379, db=0, decode_responses=True)
texas_tz = pytz.timezone('US/Central')

# --- NEW: AUTO-REFRESH EVERY 60 SECONDS ---
st_autorefresh(interval=60 * 1000, key="datarefresh")

def get_multi_history(selected_cities):
    try:
        conn = psycopg2.connect(host="aurora-postgres-service", database="postgres", user="postgres", password="fortworth")
        # Querying by the 'id' (City Name) stored in Postgres
        query = "SELECT ts, temp, lat, lon FROM soil_history ORDER BY ts DESC LIMIT 500"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

# 2. UI Layout
st.title("🌡️ Project Aurora: Texas Soil Temperatures")

raw_grid = r.get('texas_grid_data')
if raw_grid:
    grid_df = pd.DataFrame(json.loads(raw_grid))
    st.sidebar.header("Command Center")
    all_cities = grid_df['id'].tolist()
    selected_names = st.sidebar.multiselect("Select Cities to Analyze:", all_cities, default=["Fort Worth"])

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Interactive Intelligence Map")
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
        
        # --- ENHANCED MULTI-COLOR POSTGRES CHART ---
        st.divider()
        st.subheader("📈 Historical Trends (Multi-City)")
        hist_raw = get_multi_history(selected_names)
        
        if not hist_raw.empty:
            # Match coordinates to City Names from the grid_df
            # We pivot the table so columns = City Names (this triggers multi-colors)
            hist_raw['ts'] = pd.to_datetime(hist_raw['ts']).dt.tz_localize('UTC').dt.tz_convert(texas_tz)
            
            # Helper to map lat/lon back to city name
            name_map = {f"{row['lat']},{row['lon']}": row['id'] for _, row in grid_df.iterrows()}
            hist_raw['city'] = hist_raw.apply(lambda x: name_map.get(f"{x['lat']},{x['lon']}", "Unknown"), axis=1)
            
            # Filter for only selected cities and pivot
            chart_df = hist_raw[hist_raw['city'].isin(selected_names)]
            if not chart_df.empty:
                chart_pivot = chart_df.pivot_table(index='ts', columns='city', values='temp')
                st.line_chart(chart_pivot) # Streamlit automatically assigns unique colors per column!
            else:
                st.info("Gathering historical data for selected hubs...")
        else:
            st.info("Connecting to Postgres history...")

    with col2:
        # --- CST DAILY BRIEFING ---
        st.subheader("📰 AI Daily Briefing")
        if selected_names:
            now_texas = datetime.now(texas_tz)
            time_str = now_texas.strftime('%I:%M %p %Z')
            avg_temp = filtered_df['temp'].mean()
            
            st.info(f"**Texas Report:** {time_str}\n\nAvg Temp: {avg_temp:.1f}°C")
            
            st.divider()
            st.subheader("🔮 Oracle Forecast (1hr)")
            for city in selected_names:
                city_temp = filtered_df[filtered_df['id'] == city]['temp'].values[0]
                pred = round(city_temp + (np.random.uniform(-0.5, 0.5)), 2)
                st.write(f"**{city}**: {city_temp}°C → **{pred}°C**")

else:
    st.warning("Fetching Texas-wide satellite relay...")

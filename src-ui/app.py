import streamlit as st
import redis
import pandas as pd
import numpy as np
import json
import pydeck as pdk
import psycopg2
import pytz # New: Timezone support
from datetime import datetime

st.set_page_config(page_title="Aurora: Lone Star Edition", layout="wide")
r = redis.Redis(host='aurora-redis-service', port=6379, db=0, decode_responses=True)

# Define Central Time Zone
texas_tz = pytz.timezone('US/Central')

st.title("🤖 Project Aurora: The AI Oracle")

raw_grid = r.get('texas_grid_data')
if raw_grid:
    grid_df = pd.DataFrame(json.loads(raw_grid))
    st.sidebar.header("Command Center")
    selected_names = st.sidebar.multiselect("Select Cities:", grid_df['id'].tolist(), default=["Fort Worth"])

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Texas Intelligence Map")
        filtered_df = grid_df[grid_df['id'].isin(selected_names)]
        layer = pdk.Layer("ScatterplotLayer", filtered_df, pickable=True, get_position=["lon", "lat"],
                          get_radius=15000, get_fill_color="[255, 215, 0, 200]", radius_min_pixels=8)
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=pdk.ViewState(latitude=31.0, longitude=-100.0, zoom=5),
                                 tooltip={"text": "{id}: {temp}°C"}))

    with col2:
        st.subheader("📰 AI Daily Briefing")
        if selected_names:
            # NEW: Get the current time in Texas
            now_texas = datetime.now(texas_tz)
            time_str = now_texas.strftime('%I:%M %p %Z') # Format: 09:30 PM CST

            avg_temp = filtered_df['temp'].mean()
            coldest = filtered_df.loc[filtered_df['temp'].idxmin()]
            
            st.info(f"**Texas Morning Report:** It is currently **{time_str}**. "
                    f"Across your selected regions, the average soil temp is {avg_temp:.1f}°C. "
                    f"The 'Cold Spot' is **{coldest['id']}** at {coldest['temp']}°C.")
            
            st.divider()
            st.subheader("🔮 Oracle Forecast")
            for city in selected_names:
                city_temp = filtered_df[filtered_df['id'] == city]['temp'].values[0]
                pred = round(city_temp + (np.random.uniform(-0.5, 0.5)), 2)
                st.write(f"**{city}**: Now {city_temp}°C → **1hr Forecast: {pred}°C**")
        else:
            st.write("Select cities to generate a Texas-time report.")
else:
    st.warning("Booting Texas-wide satellite relay...")

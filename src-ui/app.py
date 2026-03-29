import streamlit as st
import redis
import pandas as pd
import numpy as np
import json
import pydeck as pdk
import psycopg2
from datetime import datetime, timedelta

st.set_page_config(page_title="Aurora: Oracle & Reporter", layout="wide")
r = redis.Redis(host='aurora-redis-service', port=6379, db=0, decode_responses=True)

def get_prediction(df):
    if len(df) < 5: return None
    # Simple Linear Regression Math
    y = df['temp'].values
    x = np.arange(len(y))
    slope, intercept = np.polyfit(x, y, 1)
    # Predict 3 steps into the future
    future_x = len(y) + 2
    return round(intercept + slope * future_x, 2)

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
            avg_temp = filtered_df['temp'].mean()
            coldest = filtered_df.loc[filtered_df['temp'].idxmin()]
            
            # THE GENERATIVE REPORTER: A dynamic summary
            st.info(f"**Morning Report:** It is currently {datetime.now().strftime('%H:%M')}. "
                    f"Across your selected regions, we are seeing an average soil temp of {avg_temp:.1f}°C. "
                    f"The 'Cold Spot' is currently **{coldest['id']}** at {coldest['temp']}°C. "
                    "If current trends hold, our Oracle predicts stable conditions for the next hour.")
            
            st.divider()
            st.subheader("🔮 Oracle Forecast")
            # Predict for each selected city
            for city in selected_names:
                city_temp = filtered_df[filtered_df['id'] == city]['temp'].values[0]
                # In a real app, we'd pull Postgres history here. For now, we'll simulate the 'Brain'
                pred = round(city_temp + (np.random.uniform(-0.5, 0.5)), 2)
                st.write(f"**{city}**: Now {city_temp}°C → **1hr Forecast: {pred}°C**")
        else:
            st.write("Awaiting city selection to generate report...")

else:
    st.warning("Worker is scanning the Lone Star State...")

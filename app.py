import streamlit as st
import time
import random
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium

# Simulated data store
if "events" not in st.session_state:
    st.session_state.events = []

# Simulate a new production event
def generate_event():
    truck_id = f"T{random.randint(100,199)}"
    shift = random.choice(["Shift 1", "Shift 2", "Shift 3"])
    weight = random.randint(30, 40)  # tonnes
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lat = 23.5 + random.uniform(-0.01, 0.01)
    lon = 87.3 + random.uniform(-0.01, 0.01)
    st.session_state.events.append({
        "Truck ID": truck_id,
        "Shift": shift,
        "Weight (tonnes)": weight,
        "Timestamp": timestamp,
        "Location": f"{lat:.5f}, {lon:.5f}",
        "lat": lat,
        "lon": lon
    })

st.set_page_config(page_title="Coal Mine Blockchain Demo", layout="wide")
st.title("🚜 Real-Time Coal Production Reporting (Simulated)")

# Generate new data every time page is refreshed
generate_event()

# Display dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Production Logs (latest 10)")
    df = pd.DataFrame(st.session_state.events[-10:])
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("🛰️ Live Truck Location Map")
    m = folium.Map(location=[23.5, 87.3], zoom_start=13)
    for event in st.session_state.events[-10:]:
        folium.Marker(
            location=[event["lat"], event["lon"]],
            popup=f"{event['Truck ID']} | {event['Weight (tonnes)']}t",
            icon=folium.Icon(color="blue", icon="truck", prefix="fa")
        ).add_to(m)
    st_folium(m, width=700, height=400)

# Shift-wise summary
st.subheader("📊 Shift-wise Production Summary")
summary = pd.DataFrame(st.session_state.events).groupby("Shift")["Weight (tonnes)"].sum().reset_index()
st.bar_chart(summary.set_index("Shift"))

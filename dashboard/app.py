import streamlit as st

# Dashboard Title
st.title("🚀 Mars Rover Mission Control")

# Intro text
st.write("Welcome to Mission Control Dashboard")

# Telemetry
st.header("Telemetry")

col1, col2 = st.columns(2)

with col1:
    st.metric("X Coordinate", 0)
    st.metric("Battery", "100%")

with col2:
    st.metric("Y Coordinate", 0)
    st.metric("Temperature", "25°C")

st.divider()

# Terrain Map section
st.header("Terrain Map")

st.info("Mars terrain visualization will appear here")

# Mission Logs section
st.header("Mission Logs")

st.text("Waiting for rover telemetry...")
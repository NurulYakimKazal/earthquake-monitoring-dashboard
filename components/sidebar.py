import streamlit as st
from datetime import datetime


def sidebar(stats):
    st.sidebar.header("Filters")

    view_mode = st.sidebar.selectbox(
        "View mode",
        ["Scatter", "Heatmap", "Hexagon", "3D Scatter"],
        key="view_mode"
    )

    mag_range = st.sidebar.slider(
        "Magnitude",
        0.0, 10.0,
        step=0.1,
        key="mag_range"
    )

    max_depth = st.sidebar.slider(
        "Max depth (km)",
        0, 700,
        step=10,
        key="max_depth"
    )

    mag_min, mag_max = mag_range

    # =========================
    # TIME RANGE FROM DATASET
    # =========================
    st.sidebar.subheader("Time filter")

    earliest = stats["earliest"]
    latest_time = stats["latest_time"]

    min_date = earliest.date()
    max_date = latest_time.date()

    time_range = st.sidebar.date_input(
        "Date range (Only full range applied)",
        min_value=min_date,
        max_value=max_date,
        key="time_range"
    )

    # SAFE PARSING
    if isinstance(time_range, tuple) and len(time_range) == 2:
        start_date, end_date = time_range
    else:
        start_date, end_date = min_date, max_date

    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())

    return {
        "view_mode": view_mode,
        "mag_min": mag_min,
        "mag_max": mag_max,
        "max_depth": max_depth,
        "start_time": start_time,
        "end_time": end_time,
    }
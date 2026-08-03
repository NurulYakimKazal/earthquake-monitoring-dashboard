import streamlit as st
from datetime import datetime


def sidebar(stats):
    st.sidebar.header("Filters")

    mag_range = st.sidebar.slider(
        "Magnitude",
        min_value=0.0,
        max_value=10.0,
        value=(3.0, 7.5),
        step=0.1,
    )

    max_depth = st.sidebar.slider(
        "Max depth (km)",
        min_value=0,
        max_value=700,
        value=300,
        step=10,
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

        # Save the last complete range
        st.session_state["last_valid_date_range"] = (
            start_date,
            end_date,
        )
    else:
        start_date, end_date = st.session_state.get(
            "last_valid_date_range",
            (min_date, max_date),
        )

    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())

    return {
        "mag_min": mag_min,
        "mag_max": mag_max,
        "max_depth": max_depth,
        "start_time": start_time,
        "end_time": end_time,
    }
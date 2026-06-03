import streamlit as st


def sidebar():
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

    return {
        "view_mode": view_mode,
        "mag_min": mag_min,
        "mag_max": mag_max,
        "max_depth": max_depth
    }
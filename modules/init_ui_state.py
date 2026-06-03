import streamlit as st


def init_ui_state():
    defaults = {
        "view_mode": "Scatter",
        "mag_range": (2.5, 7.5),
        "max_depth": 300
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
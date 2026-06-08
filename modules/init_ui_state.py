import streamlit as st


def init_ui_state(stats):

    earliest = stats["earliest"].date()
    latest_time = stats["latest_time"].date()

    # ensure existing state is valid BEFORE defaults
    if "time_range" in st.session_state:
        start, end = st.session_state["time_range"]

        start = max(start, earliest)
        end = min(end, latest_time)

        if start > end:
            start, end = earliest, latest_time

        st.session_state["time_range"] = (start, end)

    defaults = {
        # =========================
        # MAP UI
        # =========================
        "view_mode": "Scatter",
        "mag_range": (3, 7.5),
        "max_depth": 300,

        # =========================
        # TIME FILTER UI
        # =========================
        "time_range": (
            earliest,
            latest_time
        ),

        # =========================
        # ML UI
        # =========================
        "ml_algorithm": "HDBSCAN",
        "dbscan_eps_km": 30,
        "dbscan_min_samples": 5,
        "hdb_min_cluster_size": 8,
        "hdb_min_samples": 5,
        "show_noise": True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
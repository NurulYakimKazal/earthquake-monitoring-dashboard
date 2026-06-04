import streamlit as st


def init_ui_state():
    defaults = {
        # =========================
        # MAP UI
        # =========================
        "view_mode": "Scatter",
        "mag_range": (3, 7.5),
        "max_depth": 300,

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
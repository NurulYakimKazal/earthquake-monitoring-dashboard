import streamlit as st
import pydeck as pdk

from modules.ml_data_processing import (
    run_dbscan,
    run_hdbscan,
    get_cluster_summary,
)
from components.ml_filters import ml_controls
from components.kpis import render_ml_clustering_summary


def render_ml_earthquake_map(dff):

    # =========================
    # UI CONTROLS
    # =========================
    params = ml_controls()

    st.caption(
        "Clustering uses latitude and longitude only (haversine distance). "
        "Magnitude and depth are shown for context but are not used in the model."
    )

    st.divider()

    # =========================
    # DATA CLEANING
    # =========================
    dff = dff.copy()
    dff = dff.dropna(subset=["latitude", "longitude"])

    if dff.empty:
        st.warning("No valid coordinate data available.")
        return

    # =========================
    # CLUSTERING
    # =========================
    if params["algorithm"] == "DBSCAN":
        dff = run_dbscan(
            dff,
            eps_km=params["eps_km"],
            min_samples=params["min_samples"],
        )
    else:
        dff = run_hdbscan(
            dff,
            min_cluster_size=params["min_cluster_size"],
            min_samples=params["min_samples"],
        )

    if "cluster" not in dff.columns or dff["cluster"].isna().all():
        st.warning(
            "Clustering did not produce valid results. "
            "Try adjusting parameters."
        )
        return

    # =========================
    # KPI SUMMARY
    # =========================
    summary = get_cluster_summary(dff)
    render_ml_clustering_summary(summary)

    st.divider()

    st.caption("⚠️ ML clustering view supports scatter only.")

    # =========================
    # FILTER NOISE
    # =========================
    if not params["show_noise"]:
        dff = dff[dff["cluster"] != -1]

    if dff.empty:
        st.warning(
            "No clusters found with current settings. "
            "Try adjusting parameters."
        )
        return

    # =========================
    # POINT SIZE
    # =========================
    dff["point_size"] = dff["magnitude"].fillna(0).clip(lower=1, upper=5)

    # =========================
    # COLORS
    # =========================
    palette = [
        [0, 220, 220],  # cyan (less neon than 255)
        [245, 150, 40],  # orange (still strong)
        [230, 60, 230],  # magenta (kept punchy)
        [0, 220, 90],  # green (still vivid)
        [245, 230, 60],  # yellow (bright but controlled)
        [0, 180, 230],  # blue-cyan
        [240, 90, 170],  # pink (still vivid)
    ]

    def cluster_color(cluster_id):
        if cluster_id == -1:
            return [180, 180, 180]
        return palette[int(cluster_id) % len(palette)]

    dff["cluster_color"] = dff["cluster"].apply(cluster_color)

    # =========================
    # MAP LAYER
    # =========================
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=dff,
        get_position=["longitude", "latitude"],
        get_fill_color="cluster_color",
        radius_units="pixels",
        get_radius="point_size",
        radius_min_pixels=2,
        radius_max_pixels=6,
        opacity=0.7,
        stroked=True,
        get_line_color=[0, 0, 0],
        line_width_min_pixels=1.5,
        filled=True,
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 255, 0]
    )

    # =========================
    # VIEW STATE
    # =========================
    view_state = pdk.ViewState(
        latitude=dff["latitude"].mean(),
        longitude=dff["longitude"].mean(),
        zoom=3,
        pitch=0,
    )

    # =========================
    # TOOLTIP
    # =========================
    tooltip = {
        "html": """
            <b>Cluster:</b> {cluster}<br/>
            <b>Magnitude:</b> {magnitude}<br/>
            <b>Depth:</b> {depth} km<br/>
            <b>Location:</b> {place}
        """,
        "style": {
            "backgroundColor": "#111827",
            "color": "white",
            "padding": "10px",
            "borderRadius": "8px",
        },
    }

    # =========================
    # RENDER MAP
    # =========================
    deck = pdk.Deck(
        map_style="dark",
        layers=[scatter_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(deck, width="stretch")
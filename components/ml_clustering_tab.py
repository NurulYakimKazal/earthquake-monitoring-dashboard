import streamlit as st
import pydeck as pdk

from modules.ml_data_processing import run_dbscan, run_hdbscan, get_cluster_summary
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
    # CLEAN DATA
    # =========================
    dff = dff.copy()
    dff = dff.dropna(subset=["latitude", "longitude"])

    if dff.empty:
        st.warning("No valid coordinate data available.")
        return

    # =========================
    # ML STEP
    # =========================
    if params["algorithm"] == "DBSCAN":
        dff = run_dbscan(
            dff,
            eps_km=params["eps_km"],
            min_samples=params["min_samples"]
        )
    else:
        dff = run_hdbscan(
            dff,
            min_cluster_size=params["min_cluster_size"],
            min_samples=params["min_samples"]
        )

    # =========================
    # VALIDATION (IMPORTANT)
    # =========================
    if "cluster" not in dff.columns or dff["cluster"].isna().all():
        st.warning("Clustering did not produce valid results. Try adjusting parameters.")
        return

    # =========================
    # CLUSTER SUMMARY
    # =========================
    summary = get_cluster_summary(dff)
    render_ml_clustering_summary(summary)

    st.divider()

    # =========================
    # INFO (VISUALIZATION CONTEXT)
    # =========================
    st.caption("⚠️ ML clustering view supports scatter only.")

    # =========================
    # NOISE FILTER (-1) FOR DISPLAY ONLY
    # =========================
    if not params["show_noise"]:
        dff = dff[dff["cluster"] != -1]

    if dff.empty:
        st.warning("No clusters found with current settings. Try adjusting parameters.")
        return

    # =========================
    # FEATURE ENGINEERING
    # =========================
    dff["radius"] = (dff["magnitude"] ** 2 * 2000).clip(lower=8000)
    dff["elevation"] = dff["magnitude"] * 10000

    # =========================
    # COLOR MAP
    # =========================
    palette = [
        [0, 255, 255],
        [255, 165, 0],
        [255, 0, 255],
        [0, 255, 0],
        [255, 255, 0],
        [0, 200, 255],
        [255, 105, 180],
    ]

    def cluster_color(c):
        if c == -1:
            return [180, 180, 180]
        return palette[int(c) % len(palette)]

    dff["cluster_color"] = dff["cluster"].apply(cluster_color)

    # =========================
    # MAP
    # =========================
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=dff,
            get_position=["longitude", "latitude"],
            get_fill_color="cluster_color",
            get_radius="radius",
            opacity=0.85,
            pickable=True,
        )
    ]

    view_state = pdk.ViewState(
        latitude=dff["latitude"].mean(),
        longitude=dff["longitude"].mean(),
        zoom=3,
        pitch=0,
    )

    tooltip = {
        "html": """
            <b>Cluster:</b> {cluster}<br/>
            <b>Magnitude:</b> {magnitude}<br/>
            <b>Depth:</b> {depth} km<br/>
            <b>Location:</b> {place}
        """,
        "style": {"backgroundColor": "black", "color": "white"}
    }

    deck = pdk.Deck(
        map_style="dark",
        layers=layers,
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(deck, width='stretch')
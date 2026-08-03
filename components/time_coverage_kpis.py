import streamlit as st
from components.kpis import render_kpis_without_border


def render_latest_earthquake(latest_data):
    st.markdown("### ⚠️ Latest Earthquake")

    st.markdown(
        f"""
        **Magnitude:** {latest_data["magnitude"]}  
        **Location:** {latest_data["place"]}  
        **Depth:** {latest_data["depth"]} km  
        **Time (UTC):** {latest_data["datetime"]}  
        """
    )


def render_time_coverage(time_coverage_kpi_values):
    st.markdown("### ⏱️ Time Coverage")

    render_kpis_without_border(time_coverage_kpi_values)
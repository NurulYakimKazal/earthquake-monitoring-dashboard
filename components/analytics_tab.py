import streamlit as st
import pandas as pd
from modules.plots import (
    render_frequency_chart,
    render_magnitude_over_time,
    render_rolling_average,
    render_depth_distribution,
    render_magnitude_distribution,
)

def render_trends(dff):
    st.subheader("Seismic Data Analysis")

    df_trend = dff.copy()
    df_trend["time"] = pd.to_datetime(df_trend["time"], unit="ms", errors="coerce")

    # --- Charts ---
    freq_chart = render_frequency_chart(df_trend)
    rolling_chart = render_rolling_average(df_trend)
    mag_time_chart = render_magnitude_over_time(df_trend)
    depth_chart = render_depth_distribution(df_trend)
    mag_dist_chart = render_magnitude_distribution(df_trend)

    # --- Layout ---
    col1, col2 = st.columns(2, border=True)
    with col1:
        st.altair_chart(freq_chart, width='stretch')
    with col2:
        st.altair_chart(rolling_chart, width='stretch')

    with st.container(border=True):
        st.altair_chart(mag_time_chart, width='stretch')

    col3, col4 = st.columns(2, border=True)
    with col3:
        st.altair_chart(depth_chart, width='stretch')
    with col4:
        st.altair_chart(mag_dist_chart, width='stretch')
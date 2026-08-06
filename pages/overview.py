import streamlit as st
from components.header import render_page_title
from components.time_coverage_kpis import render_latest_earthquake, render_time_coverage
from components.kpis import render_kpis_with_border
from components.one_map_plot_container import render_one_map_plot_container
from components.footer import render_footer
from components.spacer import spacer
from modules.global_stats import prepare_global_stats
from modules.seismic_data_kpis import prepare_seismic_kpis
from modules.earthquake_map import render_earthquake_map


unfiltered_data = st.session_state.unfiltered_df
filtered_data = st.session_state.filtered_df

global_stats_value = prepare_global_stats(unfiltered_data)
latest_data = global_stats_value["latest_data"]
time_coverage_kpi_values = {
    "Start Time": global_stats_value['earliest'],
    "Latest Time": global_stats_value["latest_time"],
}

seismic_kpis = prepare_seismic_kpis(filtered_data)
earthquake_map = render_earthquake_map(filtered_data, unfiltered_data)


def overview():

    render_page_title("📊 Dashboard Overview")

    col1, col2 = st.columns([1.1, 1.9], gap="xsmall", border=True)
    with col1:
        render_latest_earthquake(latest_data)

    with col2:
        render_time_coverage(time_coverage_kpi_values)

    spacer(1)

    st.markdown("#### Seismic Data Summary")

    render_kpis_with_border(seismic_kpis)

    st.divider()

    render_one_map_plot_container("Earthquakes Map", earthquake_map)

    render_footer()


overview()
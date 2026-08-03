import streamlit as st
from components.header import render_page_title
from components.one_map_plot_container import render_one_map_plot_container
from components.chart_grid_container import render_chart_grid_container
from components.footer import render_footer
from utils.spacer import spacer
from modules.analytics_plots import (
    render_frequency_chart,
    render_rolling_average,
    render_magnitude_over_time,
    render_magnitude_distribution,
    render_depth_distribution
)

unfiltered_data = st.session_state.unfiltered_df
filtered_data = st.session_state.filtered_df

frequency_chart = render_frequency_chart(filtered_data)
rolling_average_chart = render_rolling_average(filtered_data)

magnitude_over_time_chart = render_magnitude_over_time(filtered_data)

magnitude_distribution_chart = render_magnitude_distribution(filtered_data)
depth_distribution_chart = render_depth_distribution(filtered_data)


def analytics():

    render_page_title("📈 Statistical Analytics")

    render_chart_grid_container(
        [
            ("Earthquake Frequency Over Time", frequency_chart),
            ("7-Day Rolling Average Magnitude", rolling_average_chart),
        ]
    )

    spacer(2)

    render_one_map_plot_container("Magnitude Over Time", magnitude_over_time_chart)

    spacer(2)

    render_chart_grid_container(
        [
            ("Magnitude Distribution", magnitude_distribution_chart),
            ("Depth Distribution", depth_distribution_chart)
        ]
    )

    render_footer()


analytics()
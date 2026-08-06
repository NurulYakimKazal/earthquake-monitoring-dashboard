import streamlit as st
from components.header import render_page_title
from components.ml_filters import render_ml_parameter
from components.kpis import render_kpis_with_border
from components.one_map_plot_container import render_one_map_plot_container
from components.footer import render_footer
from components.spacer import spacer
from modules.ml_data_processing import (
    prepare_clustered_data,
    get_cluster_summary,
)
from modules.clustering_map import render_ml_cluster_map

filtered_data = st.session_state.filtered_df

def ml_clustering():

    render_page_title("🧩 Machine Learning Clustering")

    st.caption(
        "Clustering uses latitude and longitude only (haversine distance). "
        "Magnitude and depth are shown for context but are not used in the model."
    )

    parameters = render_ml_parameter()

    dff = prepare_clustered_data(
        filtered_data, parameters
    )

    summary = get_cluster_summary(dff)

    spacer(2)

    st.markdown("#### Earthquake Cluster Analysis & Visualization")

    render_kpis_with_border(summary)

    st.divider()

    clustering_map = render_ml_cluster_map(dff, parameters['show_noise'])

    render_one_map_plot_container("ML Clustering Map", clustering_map)

    render_footer()


ml_clustering()

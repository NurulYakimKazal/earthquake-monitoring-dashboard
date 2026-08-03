import streamlit as st


def render_ml_parameter():
    with st.container(border=True):
        st.markdown("#### ML Clustering Controls")

        col1, col2, col3 = st.columns(3, gap='large')

        # =========================
        # COLUMN 1: BASIC CONTROLS
        # =========================
        with col1:
            algorithm = st.selectbox(
                "Clustering Algorithm",
                ["HDBSCAN", "DBSCAN"],
                index=0
            )

            show_noise = st.checkbox(
                "Show noise (Cluster: -1)",
                value=True
            )

        # =========================
        # COLUMN 2: DBSCAN CONTROLS
        # =========================
        with col2:
            if algorithm == "HDBSCAN":
                min_cluster_size = st.slider(
                    "HDBSCAN min cluster size",
                    min_value=3,
                    max_value=50,
                    value=8
                )
            else:
                eps_km = st.slider(
                    "DBSCAN eps (km)",
                    min_value=5,
                    max_value=100,
                    value=30
                )

        # =========================
        # COLUMN 3: HDBSCAN CONTROLS
        # =========================
        with col3:
            if algorithm == "HDBSCAN":
                min_samples = st.slider(
                    "HDBSCAN min samples",
                    min_value=1,
                    max_value=20,
                    value=5
                )
            else:
                min_samples = st.slider(
                    "DBSCAN min samples",
                    min_value=2,
                    max_value=20,
                    value=5
                )

        # =========================
        # RETURN VALUES
        # =========================
        if algorithm == "HDBSCAN":
            return {
                "algorithm": algorithm,
                "show_noise": show_noise,
                "min_cluster_size": min_cluster_size,
                "min_samples": min_samples
            }

        else:
            return {
                "algorithm": algorithm,
                "show_noise": show_noise,
                "eps_km": eps_km,
                "min_samples": min_samples
            }
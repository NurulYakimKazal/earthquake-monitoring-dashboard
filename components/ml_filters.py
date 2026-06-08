import streamlit as st


def ml_controls():
    with st.container(border=True):
        st.subheader("ML Clustering Controls")

        col1, col2, col3 = st.columns(3, gap='large')

        # =========================
        # COLUMN 1: BASIC CONTROLS
        # =========================
        with col1:
            algorithm = st.selectbox(
                "Clustering Algorithm",
                ["HDBSCAN", "DBSCAN"],
                key="ml_algorithm"
            )

            show_noise = st.checkbox(
                "Show noise (Cluster: -1)",
                key="show_noise"
            )

        # =========================
        # COLUMN 2: DBSCAN CONTROLS
        # =========================
        with col2:
            if algorithm == "HDBSCAN":
                min_cluster_size = st.slider(
                    "HDBSCAN min cluster size",
                    3, 50,
                    key="hdb_min_cluster_size"
                )
            else:
                eps_km = st.slider(
                    "DBSCAN eps (km)",
                    5, 100,
                    key="dbscan_eps_km"
                )

        # =========================
        # COLUMN 3: HDBSCAN CONTROLS
        # =========================
        with col3:
            if algorithm == "HDBSCAN":
                min_samples = st.slider(
                    "HDBSCAN min samples",
                    1, 20,
                    key="hdb_min_samples"
                )
            else:
                min_samples = st.slider(
                    "DBSCAN min samples",
                    2, 20,
                    key="dbscan_min_samples"
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
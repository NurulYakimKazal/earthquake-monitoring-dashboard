import streamlit as st


def render_latest_earthquake(latest_data):
    st.subheader("⚠️ Latest Earthquake")

    st.markdown(
        f"""
        **Magnitude:** {latest_data['magnitude']:.2f}  
        **Location:** {latest_data['place']}  
        **Depth:** {latest_data['depth']:.2f} km  
        **Time (UTC):** {latest_data['datetime'].strftime("%Y-%m-%d %H:%M:%S")}
        """
    )


def render_time_coverage(earliest, latest_time):
    st.subheader("⏱️ Time Coverage")

    t1, t2 = st.columns(2)

    with t1:
        st.metric("Start Time", earliest.strftime("%Y-%m-%d %H:%M:%S"))

    with t2:
        st.metric("Latest Time", latest_time.strftime("%Y-%m-%d %H:%M:%S"))



def render_dataset_summary(dff):
    st.subheader("Seismic Data Summary")

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7, border=True)

    with col1:
        st.metric("Total Events", len(dff))

    with col2:
        st.metric("Max Mag", f"{dff['magnitude'].max():.2f}")

    with col3:
        st.metric("Min Mag", f"{dff['magnitude'].min():.2f}")

    with col4:
        st.metric("Avg Mag", f"{dff['magnitude'].mean():.2f}")

    with col5:
        st.metric("Max Depth (km)", f"{dff['depth'].max():.2f}")

    with col6:
        st.metric("Min Depth (km)", f"{dff['depth'].min():.2f}")

    with col7:
        st.metric("Avg Depth (km)", f"{dff['depth'].mean():.2f}")


def render_ml_clustering_summary(summary):
    st.subheader("Earthquake Cluster Analysis & Visualization")

    col1, col2, col3 = st.columns(3, border=True)

    with col1:
        st.metric("Detected Clusters", summary["num_clusters"])

    with col2:
        st.metric("Noise (Unclustered)", f"{summary['noise_ratio']:.1%}")

    with col3:
        st.metric("Max Cluster Size", summary["largest_cluster"])


def render_summary(latest_data, earliest, latest_time, dff):
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])

        with col1:
            render_latest_earthquake(latest_data)

        with col2:
            render_time_coverage(earliest, latest_time)

        st.write("")
        render_dataset_summary(dff)


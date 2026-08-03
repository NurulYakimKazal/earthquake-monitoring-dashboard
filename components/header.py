import streamlit as st
from utils.spacer import spacer


def render_page_title(title):
    st.title("🌍 Earthquake Monitoring Dashboard")

    spacer(2)

    st.markdown(
        """
        **Data Source:** [USGS Earthquake Catalog API](https://earthquake.usgs.gov/fdsnws/event/1/)  
        Real-time global earthquake events provided by the United States Geological Survey (USGS).
        """
    )

    spacer(1)

    st.header(title)

    spacer(2)
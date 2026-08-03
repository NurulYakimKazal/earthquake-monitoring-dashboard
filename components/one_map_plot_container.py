import streamlit as st
from utils.spacer import spacer


def render_one_map_plot_container(title, figure):
    with st.container(border=True):
        st.markdown(f"##### {title}")

        spacer(1)

        st.plotly_chart(figure)
import streamlit as st
from components.spacer import spacer

def render_chart_grid_container(charts):
    cols = st.columns(len(charts), gap="xsmall", border=True)

    for col, (title, figure) in zip(cols, charts):
        with col:
            st.markdown(f"##### {title}")

            spacer(1)

            st.plotly_chart(figure)
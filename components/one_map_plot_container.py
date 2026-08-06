import streamlit as st


def render_one_map_plot_container(title, figure):
    with st.container(border=True, height="stretch"):
        st.markdown(f"##### {title}")

        st.plotly_chart(figure)
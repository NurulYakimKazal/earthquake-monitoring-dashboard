import streamlit as st

from components.header import render_page_title
from components.live_feed_catalog import render_live_feed, render_catalog
from components.footer import render_footer
from modules.live_feed_catalog_processing import prepare_live_feed_data, prepare_catalog_data


unfiltered_data = st.session_state.unfiltered_df
feed = prepare_live_feed_data(unfiltered_data)
display_df = prepare_catalog_data(unfiltered_data.head(500))


def catalog():

    render_page_title("📡 Live Feed & Catalog")

    col1, col2 = st.columns([1, 2], gap="small", border=True)
    with col1:
        render_live_feed(feed)

    with col2:
        render_catalog(display_df)

    render_footer()


catalog()
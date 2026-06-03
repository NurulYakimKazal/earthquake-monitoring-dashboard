import streamlit as st
import time


def init_db_and_sync(create_tables, run_etl):
    create_tables()

    now = time.time()
    last_run = st.session_state.get("last_etl_run", 0)

    if now - last_run > 60:
        try:
            # noinspection PyTypeChecker
            with st.spinner("Syncing earthquake data..."):
                run_etl()

            st.session_state.last_etl_run = now

        except Exception as e:
            st.warning(f"Data sync failed: {e}")
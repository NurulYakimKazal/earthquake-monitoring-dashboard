import streamlit as st

def init_ui_state(stats):

    earliest = stats["earliest"].date()
    latest_time = stats["latest_time"].date()

    # =========================
    # SAFE TIME STATE NORMALIZATION
    # =========================
    if "time_range" not in st.session_state:
        st.session_state["time_range"] = (earliest, latest_time)

    else:
        raw = st.session_state["time_range"]

        # ONLY update when fully valid range exists
        if isinstance(raw, tuple) and len(raw) == 2:
            start, end = raw

            start = max(start, earliest)
            end = min(end, latest_time)

            if start <= end:
                st.session_state["time_range"] = (start, end)
            else:
                st.session_state["time_range"] = (end, start)
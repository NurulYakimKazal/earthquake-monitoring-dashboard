import streamlit as st


def render_kpis_with_border(kpis):
    cols = st.columns(len(kpis), gap="xsmall", border=True)

    for col, (label, value) in zip(cols, kpis.items()):
        with col:
            st.metric(label, value)



def render_kpis_without_border(kpis):
    cols = st.columns(len(kpis), border=False)

    for col, (label, value) in zip(cols, kpis.items()):
        with col:
            st.metric(label, value)
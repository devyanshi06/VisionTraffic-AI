import streamlit as st
from datetime import datetime


def render_header():

    current_time = datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")

    left, right = st.columns([5, 2])

    with left:
        st.markdown(
            """
            # 🚦 VisionTraffic AI
            ### Smart Traffic Monitoring & Analytics Dashboard
            """
        )

    with right:
        st.metric(
            label="🕒 Current Time",
            value=current_time
        )

    st.info(
        "AI-powered traffic monitoring system for congestion detection, vehicle analytics, and smart traffic management."
    )

    st.divider()
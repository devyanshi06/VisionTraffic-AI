import streamlit as st


def render_camera():

    st.subheader("📹 Live Camera Feed")

    st.info("Waiting for backend stream...")

    st.image(
        "assets/traffic_placeholder.jpg",
        use_container_width=True
    )
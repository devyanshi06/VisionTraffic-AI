import streamlit as st

def render_sidebar():

    st.sidebar.title("🚦 VisionTraffic AI")

    camera = st.sidebar.selectbox(
        "Select Camera Feed",
        [
            "Intersection A",
            "Intersection B",
            "Highway NH-27",
            "City Center"
        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.success("🟢 Dashboard Online")
    st.sidebar.success("🟢 Camera Connected")
    st.sidebar.success("🟢 AI Ready")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Project Team")

    st.sidebar.write("👨‍💻 Frontend Developer")

    st.sidebar.write("🤖 ML Developer")

    st.sidebar.markdown("---")

    st.sidebar.caption("Version 1.0")

    return camera
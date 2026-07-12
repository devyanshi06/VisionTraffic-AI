import streamlit as st
import pandas as pd
import numpy as np

# -----------------------
# Page Configuration
# -----------------------

st.set_page_config(
    page_title="VisionTraffic AI",
    page_icon="🚦",
    layout="wide"
)

# -----------------------
# Sidebar
# -----------------------

st.sidebar.title("🚦 VisionTraffic AI")

camera = st.sidebar.selectbox(
    "Select Camera",
    [
        "Intersection A",
        "Intersection B",
        "Highway",
        "City Center"
    ]
)

st.sidebar.success("System Online")

st.sidebar.markdown("---")

st.sidebar.write("### Current Status")

st.sidebar.write("🟢 Camera Connected")
st.sidebar.write("🟢 AI Detection Running")
st.sidebar.write("🟢 Dashboard Active")

# -----------------------
# Main Heading
# -----------------------

st.title("🚦 Smart Transport Operations Dashboard")

st.write("Real-time traffic monitoring powered by AI")

st.divider()

# -----------------------
# Metric Cards
# -----------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vehicles", "142", "+12")

col2.metric("Congestion", "Medium")

col3.metric("Average Speed", "46 km/h")

col4.metric("Emergency Alerts", "1")

st.divider()

# -----------------------
# Main Layout
# -----------------------

left, right = st.columns([2,1])

with left:

    st.subheader("📷 Live Camera Feed")

    st.info("YOLO processed video will appear here.")

    st.image(
        "https://placehold.co/900x500?text=Traffic+Camera+Feed",
        use_container_width=True
    )

with right:

    st.subheader("Traffic Analytics")

    df = pd.DataFrame(
        np.random.randint(20,80,(20,2)),
        columns=["Lane A","Lane B"]
    )

    st.line_chart(df)

    st.subheader("Traffic Status")

    st.success("Traffic is flowing normally.")

st.divider()

st.subheader("🚨 Recent Alerts")

st.warning("Heavy traffic detected near Junction 3.")

st.info("Signal optimization activated.")

st.error("Emergency vehicle detected on Highway.")
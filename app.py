import streamlit as st

from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.charts import render_charts

from utils.mock_data import get_dashboard_data


st.set_page_config(
    page_title="VisionTraffic AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

camera = render_sidebar()

data = get_dashboard_data()

vehicle_count = data["vehicle_count"]
traffic_status = data["traffic_status"]
average_speed = data["average_speed"]
alerts = data["alerts"]

st.title("🚦 VisionTraffic AI")

st.markdown("""
### Smart Transport Operations Dashboard

Monitor city traffic in real time using AI-powered vehicle detection and analytics.
""")

st.divider()

render_metrics(
    vehicle_count,
    traffic_status,
    average_speed,
    alerts
)

st.divider()

left, center, right = st.columns([2.3, 1.2, 1])

with left:

    st.subheader("📹 Live Camera Feed")

    st.info("Backend will stream processed YOLO video here.")

    st.image(
        "assets/traffic_placeholder.jpg",
        use_container_width=True
    )

with center:

    render_charts()

with right:

    st.subheader("🚨 Live Alerts")

    st.success("Signal timings optimized")

    st.warning("Heavy traffic near Junction A")

    st.info("Emergency lane clear")

    st.error("Accident reported near NH-27")

st.divider()

st.subheader("🤖 AI Recommendations")

c1, c2 = st.columns(2)

with c1:

    st.success("✅ Divert traffic to Ring Road.")

    st.success("✅ Increase green signal by 15 seconds.")

    st.success("✅ Prioritize ambulance route.")

with c2:

    st.info("Traffic expected to increase after 6 PM.")

    st.info("Construction work causing slow movement.")

    st.info("Alternate route updated.")

st.divider()

st.caption(
    "VisionTraffic AI • Built using Streamlit + YOLOv8"
)
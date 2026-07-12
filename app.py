import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ==============================
# COMPONENTS
# ==============================

from components.header import render_header
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.charts import render_charts
from components.camera import render_camera
from components.alerts import render_alerts
from components.recommendations import render_recommendations
from components.vehicle_distribution import render_vehicle_distribution
from components.events import render_events

# ==============================
# DATA
# ==============================

from utils.mock_data import get_dashboard_data

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="VisionTraffic AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# AUTO REFRESH
# ==============================

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

# ==============================
# LOAD CSS
# ==============================

def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


load_css()

# ==============================
# SIDEBAR
# ==============================

selected_camera = render_sidebar()

# ==============================
# FETCH DATA
# ==============================

data = get_dashboard_data()

vehicle_count = data["vehicle_count"]
traffic_status = data["traffic_status"]
average_speed = data["average_speed"]
alerts = data["alerts"]

# ==============================
# HEADER
# ==============================

render_header()

# ==============================
# METRICS
# ==============================

render_metrics(
    vehicle_count,
    traffic_status,
    average_speed,
    alerts
)

st.divider()

# ==============================
# MAIN DASHBOARD
# ==============================

camera_col, chart_col, alert_col = st.columns([2.5, 1.3, 1])

with camera_col:
    render_camera()

with chart_col:
    render_charts()

with alert_col:
    render_alerts()

st.divider()

# ==============================
# SECOND ROW
# ==============================

distribution_col, events_col = st.columns([1, 1])

with distribution_col:
    render_vehicle_distribution()

with events_col:
    render_events()

st.divider()

# ==============================
# AI RECOMMENDATIONS
# ==============================

render_recommendations()

st.divider()

# ==============================
# SYSTEM STATUS
# ==============================

st.subheader("🖥️ System Status")

status1, status2, status3, status4 = st.columns(4)

status1.success("🟢 Dashboard Online")
status2.success("🟢 AI Model Ready")
status3.success("🟢 Camera Connected")
status4.success("🟢 Backend Connected")

st.divider()

# ==============================
# FOOTER
# ==============================

st.markdown(
    """
---
### 🚦 VisionTraffic AI

AI-powered Smart Traffic Monitoring Dashboard

**Technology Stack**

- 🐍 Python
- 🚦 Streamlit
- 🤖 YOLOv8
- 🎥 OpenCV
- ⚡ FastAPI (Backend Integration)
- 📊 Pandas & NumPy

Made for Hackathon 2026
"""
)
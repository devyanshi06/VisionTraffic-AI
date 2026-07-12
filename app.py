import streamlit as st
import pandas as pd
import numpy as np
import time

# 🎨 IMPORT FRONTEND WIDGETS
from components.header import render_header
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.charts import render_charts
from components.camera import render_camera
from components.alerts import render_alerts
from components.recommendations import render_recommendations
from components.vehicle_distribution import render_vehicle_distribution
from components.events import render_events
from utils.mock_data import get_dashboard_data

# 🧠 IMPORT THE DECOUPLED BACKEND CALCULATIONS ENGINE
from backend import TrafficAnalyticsEngine

# ==============================
# GLOBAL STRUCTURE CONFIGURATIONS
# ==============================
st.set_page_config(
    page_title="VisionTraffic AI", 
    page_icon="🚦", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Load layout styling assets smoothly
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Render modular layout components from your teammate's architecture
selected_camera = render_sidebar()
render_header()

# ==============================
# DYNAMIC ROUTING ENVIRONMENT
# ==============================
# Triggers the live AI counting engine automatically on the default selection
if selected_camera == "Intersection A":
    engine = TrafficAnalyticsEngine(video_source="traffic.mp4")
    
    # Establish container slots inside your friend's exact grid architecture
    metrics_placeholder = st.empty()
    st.divider()
    
    camera_col, chart_col, alert_col = st.columns([2.5, 1.3, 1])
    with camera_col:
        st.subheader("🎥 Live Feed Analytics")
        video_placeholder = st.empty()
    with chart_col:
        st.subheader("📈 Accumulation Profile")
        chart_placeholder = st.empty()
    with alert_col:
        st.subheader("⚠️ System Alerts")
        alert_placeholder = st.empty()
        
    st.divider()
    distribution_col, events_col = st.columns([1, 1])
    with distribution_col:
        st.subheader("📊 Vehicle Fleet Distribution")
        dist_placeholder = st.empty()
    with events_col:
        st.subheader("📋 Recent Network Events")
        events_placeholder = st.empty()

    chart_history = []

    # UI presentation rendering loop calling the backend engine
    while True:
        telemetry_payload = engine.process_next_frame(conf_threshold=0.25)
        
        if telemetry_payload is None:
            # 🔄 AUTO-REWIND: If the video reaches the end, reset it automatically
            engine.close()
            engine = TrafficAnalyticsEngine(video_source="traffic.mp4")
            continue

        current_count = telemetry_payload["count"]
        frame_idx = telemetry_payload["frame_idx"]

        # Calculate localized dashboard variables dynamically from live numbers
        if current_count < 15:
            flow_status, avg_speed = "🟢 Optimal Flow", "62 km/h"
        elif 15 <= current_count < 35:
            flow_status, avg_speed = "🟡 Moderate Volume", "45 km/h"
        else:
            flow_status, avg_speed = "🔴 Gridlock Warning", "18 km/h"

        # Inject real processing numbers straight into your friend's metric components
        with metrics_placeholder.container():
            render_metrics(
                vehicle_count=current_count,
                traffic_status=flow_status,
                average_speed=avg_speed,
                alerts=1 if current_count >= 35 else 0
            )

        # Stream the dynamic analytics frame directly to their camera block position
        video_placeholder.image(telemetry_payload["frame"], use_container_width=True)

        # Smoothly cycle auxiliary chart and alert elements periodically
        chart_history.append(current_count)
        if len(chart_history) > 50:
            chart_history.pop(0)

        if frame_idx % 5 == 0:
            with chart_placeholder.container():
                render_charts()
            with alert_placeholder.container():
                render_alerts()
            with dist_placeholder.container():
                render_vehicle_distribution()
            with events_placeholder.container():
                render_events()

        # ⚡ CRITICAL UI PACING: Gives the frontend a brief moment to render the video frame
        time.sleep(0.03)

    engine.close()

else:
    # FALLBACK PRESENTATION MODE: Handles other nodes using your friend's original structure
    data = get_dashboard_data()
    render_metrics(data["vehicle_count"], data["traffic_status"], data["average_speed"], data["alerts"])
    st.divider()
    
    camera_col, chart_col, alert_col = st.columns([2.5, 1.3, 1])
    with camera_col:
        st.subheader("🎥 Live Feed Analytics")
        # Safe catch block in case assets/traffic_placeholder.jpg path fails locally
        try:
            render_camera()
        except Exception:
            st.image(
                "https://images.unsplash.com/photo-1545179605-129665d612e3?q=80&w=720&auto=format&fit=crop", 
                caption="🔒 Node Telemetry Offline - Displaying Network Backup Feed...",
                use_container_width=True
            )
    with chart_col:
        st.subheader("📈 Accumulation Profile")
        render_charts()
    with alert_col:
        st.subheader("⚠️ System Alerts")
        render_alerts()
    
    st.divider()
    distribution_col, events_col = st.columns([1, 1])
    with distribution_col:
        st.subheader("📊 Vehicle Fleet Distribution")
        render_vehicle_distribution()
    with events_col:
        st.subheader("📋 Recent Network Events")
        render_events()

# ==============================
# AI RECOMMENDATIONS & GLOBAL STATUS FOOTER
# ==============================
st.divider()
render_recommendations()

st.divider()
st.subheader("🖥️ System Status")
status1, status2, status3, status4 = st.columns(4)
status1.success("🟢 Dashboard Online")
status2.success("🟢 AI Model Ready")
status3.success("🟢 Camera Connected")
status4.success("🟢 Backend Connected")
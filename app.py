import streamlit as st
import pandas as pd
import numpy as np
import cv2
from ultralytics import YOLO
import torch

# 1. Page & Branding Configuration
st.set_page_config(
    page_title="VisionTraffic AI Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for a modern dark-mode command center look
st.markdown("""
    <style>
    .main-title { font-size: 2.8rem; font-weight: 800; color: #1E88E5; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.2rem; color: #757575; margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Infrastructure
st.sidebar.title("🎮 Operations Control")
st.sidebar.markdown("---")
selected_sector = st.sidebar.selectbox(
    "Active Telemetry Node",
    ["Node 01 - Drone Aerial Feed", "Node 02 - Highway Cam B", "Node 03 - Core Intersection"]
)

# Dynamic Hardware Detection Status
device = "cuda" if torch.cuda.is_available() else "cpu"
status_color = "⚡" if device == "cuda" else "💻"

st.sidebar.markdown("---")
st.sidebar.success(f"{status_color} Target Hardware: {device.upper()}")
st.sidebar.info("🤖 Analytics Model: YOLOv8n (Double-Count Prevention Engine)")

# 3. Application Main Header Layout
st.markdown('<div class="main-title">🚦 VisionTraffic AI — Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Intelligent Top-Down Vehicle Fleet Analytics & Transit Telemetry</div>', unsafe_allow_html=True)
st.markdown("---")

# 4. Interactive Framework Workspace Spacing
left_video_col, right_graph_col = st.columns([5, 3])

with left_video_col:
    st.subheader(f"📹 Dynamic Processing Stream: {selected_sector}")
    video_placeholder = st.empty()

with right_graph_col:
    st.subheader("📊 Network Metrics Summary")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown("**Total Tracked Vehicles**")
        metric_count_slot = st.empty()
    with m_col2:
        st.markdown("**Traffic Congestion Index**")
        metric_status_slot = st.empty()
        
    st.markdown("---")
    st.markdown("📈 **Real-Time Accumulation Profile**")
    chart_placeholder = st.empty()

# 5. Core Detection Loop Pipeline Execution
if "Drone" in selected_sector:
    model = YOLO("yolov8n.pt")
    if device == "cuda":
        model.to(device)
        
    cap = cv2.VideoCapture("traffic.mp4")
    
    # ⚡ NEW: Spatial Memory Structures to lock down double counting
    counted_vehicle_footprints = []  # Stores (cx, cy, frame_timestamp)
    total_passed_count = 0
    chart_history = []
    frame_counter = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.info("🏁 Video pipeline loop cycle complete.")
            break

        frame_counter += 1
        height, width, _ = frame.shape
        
        # Define the digital horizontal gate line directly across the screen center
        counting_line_y = int(height * 0.5)

        # Standard predict engine running locally at standard pixel resolution dimensions
        results = model.predict(
            frame, 
            classes=[2, 3, 5, 7], 
            conf=0.25, 
            imgsz=640,
            device=device,
            verbose=False
        )

        boxes = results[0].boxes.xyxy.cpu().numpy()
        current_frame_centroids = []

        # Clear out old footprint locks from the tracking log array to maintain space capacity
        # Filters out any spatial locks older than 45 frame execution cycles
        counted_vehicle_footprints = [f for f in counted_vehicle_footprints if frame_counter - f[2] < 45]

        for box in boxes:
            x1, y1, x2, y2 = box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            
            # Draw highly visible structural bounding arrays manually over matrices
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Check if the vehicle centroid passes through the broad gate buffer zone
            if abs(cy - counting_line_y) < 30:
                # ⚡ CRITICAL FIX: Cross-verify point proximity against active memory arrays
                already_logged = False
                for past_cx, past_cy, _ in counted_vehicle_footprints:
                    # Euclidean pixel distance calculation
                    distance = np.hypot(cx - past_cx, cy - past_cy)
                    if distance < 65:  # If within a 65-pixel radius, it's the exact same car moving
                        already_logged = True
                        break
                
                if not already_logged:
                    total_passed_count += 1
                    # Log the spatial lock along with the current frame execution index
                    counted_vehicle_footprints.append((cx, cy, frame_counter))

        # Render the bright blue crossing lane visual directly on the display frame
        cv2.line(frame, (0, counting_line_y), (width, counting_line_y), (255, 0, 0), 4)
        cv2.putText(frame, "ACTIVE TELEMETRY CROSSING GATE", (20, counting_line_y - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Update metric windows
        metric_count_slot.markdown(f"## `{total_passed_count}` vehicles")
        
        if total_passed_count < 15:
            flow_status = "🟢 Optimal Flow"
        elif 15 <= total_passed_count < 35:
            flow_status = "🟡 Moderate Volume"
        else:
            flow_status = "🔴 Gridlock Warning"
            
        metric_status_slot.markdown(f"### {flow_status}")

        chart_history.append(total_passed_count)
        if len(chart_history) > 50:
            chart_history.pop(0)
            
        if frame_counter % 5 == 0:
            chart_placeholder.line_chart(pd.DataFrame(chart_history, columns=['Cumulative Units Logged']))

        # Downscale display dimensions to 720p width layout grid to accelerate web presentation speeds
        display_frame = cv2.resize(frame, (720, 405))

        # Convert matrix elements cleanly to allow smooth Streamlit rendering
        rgb_view = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(rgb_view, use_container_width=True)

    cap.release()
else:
    video_placeholder.warning("⚠️ Target RTSP stream offline.")
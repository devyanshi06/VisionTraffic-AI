import streamlit as st

def render_metrics(vehicle_count,
                   traffic_status,
                   average_speed,
                   alerts):

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🚗 Vehicles",
        vehicle_count,
        "+12"
    )

    c2.metric(
        "🚦 Traffic Status",
        traffic_status
    )

    c3.metric(
        "⚡ Avg Speed",
        f"{average_speed} km/h"
    )

    c4.metric(
        "🚨 Alerts",
        alerts
    )
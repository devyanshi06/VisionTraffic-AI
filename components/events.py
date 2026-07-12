import streamlit as st
import pandas as pd
from datetime import datetime

def render_events():

    st.subheader("📋 Recent Events")

    df = pd.DataFrame({

        "Time":[
            datetime.now().strftime("%H:%M"),
            datetime.now().strftime("%H:%M"),
            datetime.now().strftime("%H:%M")
        ],

        "Event":[
            "Heavy Traffic",
            "Signal Optimized",
            "Emergency Vehicle"
        ],

        "Location":[
            "Junction A",
            "NH-27",
            "City Center"
        ]

    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
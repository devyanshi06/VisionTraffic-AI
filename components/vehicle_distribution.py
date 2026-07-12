import streamlit as st
import pandas as pd
import random

def render_vehicle_distribution():

    st.subheader("🚗 Vehicle Distribution")

    data = pd.DataFrame({
        "Vehicle":[
            "Car",
            "Bike",
            "Bus",
            "Truck",
            "Auto"
        ],
        "Count":[
            random.randint(20,70),
            random.randint(10,50),
            random.randint(5,20),
            random.randint(5,20),
            random.randint(10,30)
        ]
    })

    st.bar_chart(
        data.set_index("Vehicle")
    )
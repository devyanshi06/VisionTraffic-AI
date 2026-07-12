import streamlit as st
import pandas as pd
import numpy as np
import random


def render_charts():

    st.subheader("📈 Vehicle Flow")

    chart = pd.DataFrame(
        np.random.randint(
            20,
            80,
            size=(20, 2)
        ),
        columns=[
            "Lane A",
            "Lane B"
        ]
    )

    st.line_chart(chart)

    st.subheader("Traffic Density")

    density = pd.DataFrame({

        "Vehicles": [

            random.randint(40, 90),

            random.randint(40, 90),

            random.randint(40, 90),

            random.randint(40, 90),

            random.randint(40, 90),

            random.randint(40, 90),

            random.randint(40, 90)
        ]

    })

    st.bar_chart(density)
import streamlit as st


def render_recommendations():

    st.subheader("🤖 AI Recommendations")

    left, right = st.columns(2)

    with left:

        st.success(
            "Increase green signal by 15 seconds."
        )

        st.success(
            "Redirect heavy vehicles to Ring Road."
        )

        st.success(
            "Prioritize ambulance lane."
        )

    with right:

        st.info(
            "Traffic expected to increase after 6 PM."
        )

        st.info(
            "Construction work slowing traffic."
        )

        st.info(
            "Suggested alternate routes updated."
        )
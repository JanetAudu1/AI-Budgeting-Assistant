import streamlit as st
from backEnd.recommender import generate_advice_stream
from backEnd.data_validation import UserData

def generate_advice_ui(inputs: UserData):
    advice_placeholder = st.empty()
    complete_advice = ""

    advice_placeholder.text("Generating Financial Advice...")

    try:
        for advice_chunk in generate_advice_stream(inputs):
            complete_advice += advice_chunk
            advice_placeholder.markdown(f"<div class='streamed-advice'>{complete_advice}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating advice: {str(e)}")

    if not complete_advice:
        st.warning("No advice was generated. Please check your inputs and try again.")

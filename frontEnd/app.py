import streamlit as st
import sys
from pathlib import Path
from input_handlers import handle_inputs
from layout import display_home_page, display_analysis_page
from advice import generate_advice_ui  # Delegate advice display to advice.py
from data_validation import UserData

sys.path.append(str(Path(__file__).resolve().parent.parent / 'backEnd'))

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #F5F5F5; font-family: 'Helvetica', sans-serif;}
    h1, h2, h3, h4, h5, h6 {color: #2C6E49;}
    .stButton>button {background-color: #2C6E49; color: white; border-radius: 10px; font-size: 16px;}
    .stTextInput>div>input, .stNumberInput>div>input {border-color: #2C6E49;}
    .stTextArea>label, .stTextInput>label, .stNumberInput>label {font-size: 16px; font-weight: bold; color: #333333;}
    footer {visibility: hidden;}
    .reportview-container .main .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("📊 Navigation")
options = st.sidebar.radio("Select a Section:", ["Home", "Financial Analysis"])

if options == "Home":
    display_home_page()

elif options == "Financial Analysis":
    inputs = handle_inputs()
    if inputs:
        # Generate Financial Analysis and Advice
        st.header("🔍 Financial Analysis")
        display_analysis_page(inputs)

        # Delegate to advice.py to generate and stream advice
        generate_advice_ui(inputs)

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sys
from pathlib import Path

# Add the backEnd directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'backEnd'))

from layout import display_home_page, display_analysis_page
from input_handlers import handle_inputs

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #F5F5F5; font-family: 'Helvetica', sans-serif;}
    h1, h2, h3, h4, h5, h6 {color: #2C6E49;}
    .stButton>button {background-color: #2C6E49; color: white; border-radius: 10px; font-size: 16px;}
    .stTextInput>div>input {border-color: #2C6E49;}
    .stNumberInput>div>input {border-color: #2C6E49;}
    .stTextArea>label {font-size: 16px; font-weight: bold; color: #333333;}
    .stTextInput>label {font-size: 16px; font-weight: bold; color: #333333;}
    .stNumberInput>label {font-size: 16px; font-weight: bold; color: #333333;}
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
    if inputs:  # If inputs are not empty
        display_analysis_page(inputs)


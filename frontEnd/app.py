import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'backEnd'))

from backEnd.data_validation import UserData
import streamlit as st
import pandas as pd
from layout import display_home_page, display_analysis_page
from input_handlers import handle_inputs
from advice import generate_advice_ui  # Assuming this is correct

# Custom CSS for styling (Import Roboto from Google Fonts)
st.markdown("""
    <style>
    /* Import Roboto Font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* General Background and Text Colors for Main Content */
    .main {
        background-color: #1E1E1E;
        color: #ECECEC;
        font-family: 'Roboto', sans-serif;  /* Use Roboto */
    }

    /* Sidebar Styling */
    .css-1d391kg, .css-18e3th9 {
        background-color: #252525;
        color: #ECECEC;
    }

    /* Sidebar input field styles */
    .css-1d391kg .stTextInput input, .css-1d391kg .stNumberInput input, .css-1d391kg .stTextArea textarea,
    .css-18e3th9 .stTextInput input, .css-18e3th9 .stNumberInput input, .css-18e3th9 .stTextArea textarea {
        background-color: #333;
        color: white;
        border: 1px solid #3D9970;
        font-family: 'Roboto', sans-serif;  /* Apply Roboto */
    }

    .css-1d391kg .stTextInput label, .css-1d391kg .stNumberInput label, .css-1d391kg .stTextArea label,
    .css-18e3th9 .stTextInput label, .css-18e3th9 .stNumberInput label, .css-18e3th9 .stTextArea label {
        color: #B0B0B0;
        font-weight: bold;
        font-family: 'Roboto', sans-serif;
    }

    /* Buttons */
    .stButton>button, .css-1d391kg .stButton>button, .css-18e3th9 .stButton>button {
        background-color: #3D9970;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        border: none;
        transition: background-color 0.3s ease;
        font-family: 'Roboto', sans-serif;  /* Apply Roboto */
    }

    .stButton>button:hover, .css-1d391kg .stButton>button:hover, .css-18e3th9 .stButton>button:hover {
        background-color: #2C6E49;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #ECECEC;
        font-weight: 700;
        font-family: 'Roboto', sans-serif;  /* Apply Roboto */
    }

    /* Input Fields */
    .stTextInput>div>input, .stNumberInput>div>input, .stTextArea>div>textarea {
        background-color: #333;
        color: white;
        border: 1px solid #3D9970;
        font-family: 'Roboto', sans-serif;
    }

    .stTextInput>label, .stNumberInput>label, .stTextArea>label {
        font-size: 16px;
        font-weight: bold;
        color: #B0B0B0;
    }

    /* Text for streamed advice */
    .streamed-advice {
        word-wrap: break-word;
        white-space: normal;
        font-size: 16px;
        color: #ECECEC;
        max-width: 800px;
    }

    /* Links and Hover Effects */
    a {
        color: #3D9970;
    }
    a:hover {
        color: #2C6E49;
    }

    /* Footer */
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

import streamlit as st
import sys
from pathlib import Path
from input_handlers import handle_inputs
from layout import display_home_page, display_analysis_page
from advice import generate_advice_ui  # Delegate advice display to advice.py
from data_validation import UserData

sys.path.append(str(Path(__file__).resolve().parent.parent / 'backEnd'))

# Custom CSS for dark theme and professional styling
st.markdown("""
    <style>
    /* General Background and Text Colors for Main Content */
    .main {
        background-color: #1E1E1E;
        color: #F0F0F0;
        font-family: 'Roboto', sans-serif;
    }

    /* Sidebar Styling */
    .css-1d391kg, .css-18e3th9 {
        background-color: #252525 !important;  /* Dark background for the sidebar */
        color: #ECECEC;  /* Light text color */
    }

    /* Sidebar Title and Radio Button Text */
    .css-1d391kg .stRadio label, .css-1d391kg .stTitle, .css-18e3th9 .stTitle {
        color: #ECECEC !important;  /* Ensure the sidebar titles and radio labels are light */
        font-weight: bold;
        font-size: 18px;
    }

    /* Sidebar input field styles */
    .css-1d391kg .stTextInput input, .css-1d391kg .stNumberInput input, .css-1d391kg .stTextArea textarea,
    .css-18e3th9 .stTextInput input, .css-18e3th9 .stNumberInput input, .css-18e3th9 .stTextArea textarea {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #3D9970 !important;
    }

    .css-1d391kg .stTextInput label, .css-1d391kg .stNumberInput label, .css-1d391kg .stTextArea label,
    .css-18e3th9 .stTextInput label, .css-18e3th9 .stNumberInput label, .css-18e3th9 .stTextArea label {
        color: #B0B0B0 !important;
        font-weight: bold;
    }

    /* Buttons in Main Content and Sidebar */
    .stButton>button, .css-1d391kg .stButton>button, .css-18e3th9 .stButton>button {
        background-color: #3D9970 !important;
        color: white !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        border: none !important;
        transition: background-color 0.3s ease !important;
    }

    .stButton>button:hover, .css-1d391kg .stButton>button:hover, .css-18e3th9 .stButton>button:hover {
        background-color: #2C6E49 !important;
    }

    /* Headings Styles for Main Content */
    h1, h2, h3, h4, h5, h6 {
        color: #ECECEC;
        font-weight: 700;
    }

    /* Input Fields in Main Content */
    .stTextInput>div>input, .stNumberInput>div>input, .stTextArea>div>textarea {
        background-color: #333;
        color: white;
        border: 1px solid #3D9970;
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

    /* Footer and Padding */
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

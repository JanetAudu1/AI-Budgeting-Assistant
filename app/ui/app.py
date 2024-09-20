import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from app.ui.layout import display_home_page, display_analysis_page
from app.ui.input_handlers import handle_inputs
from app.ui.advice import generate_advice_ui

# Set page config as the first Streamlit command
st.set_page_config(page_title="AI Budgeting Assistant", page_icon="💰", layout="wide")

# Custom CSS (updated)
st.markdown("""
    <style>
    body {font-family: 'Roboto', sans-serif;}
    .main {background-color: #1E1E1E; color: #ECECEC;}
    .stButton>button {background-color: #3D9970; color: white;}
    .stTextArea>div>div>textarea {height: auto !important; min-height: 100px;}
    .streamlit-expanderHeader {font-size: 16px; font-weight: bold;}
    .streamlit-expanderContent {overflow: visible !important;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar for navigation
options = st.sidebar.radio("Select a Section:", ["Home", "Budget Analysis"])

if options == "Home":
    display_home_page()
elif options == "Budget Analysis":
    inputs = handle_inputs()
    if inputs:
        display_analysis_page(inputs)
        generate_advice_ui(inputs)

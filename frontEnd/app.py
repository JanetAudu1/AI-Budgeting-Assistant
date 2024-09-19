import streamlit as st

# compulsory first Streamlit command
st.set_page_config(page_title="AI Budgeting Assistant", page_icon="💰", layout="wide")

from layout import display_home_page, display_analysis_page
from input_handlers import handle_inputs
from advice import generate_advice_ui

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
options = st.sidebar.radio("Select a Section:", ["Home", "Financial Analysis"])

if options == "Home":
    display_home_page()
elif options == "Financial Analysis":
    inputs = handle_inputs()
    if inputs:
        display_analysis_page(inputs)
        generate_advice_ui(inputs)

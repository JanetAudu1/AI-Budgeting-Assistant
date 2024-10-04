import sys
from pathlib import Path
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from app.ui.layout import display_home_page, display_analysis_page
from app.ui.input_handlers import handle_inputs
from app.ui.advice import generate_advice_ui
from app.api.models import UserDataInput
from app.services.recommender import generate_advice_stream

# Set page config as the first Streamlit command
st.set_page_config(page_title="AI Budgeting Assistant", page_icon="💰", layout="wide")

# Custom CSS (updated for dark mode)
st.markdown("""
    <style>
    .stApp {background-color: #0E1117; color: #FAFAFA;}
    .stButton>button {background-color: #3D9970; color: white;}
    .stTextArea>div>div>textarea {background-color: #262730; color: #FAFAFA;}
    .streamlit-expanderHeader {font-size: 16px; font-weight: bold; color: #FAFAFA;}
    .streamlit-expanderContent {overflow: visible !important;}
    </style>
    """, unsafe_allow_html=True)

def main():
    
    options = st.sidebar.radio("Select a Section:", ["Home", "Budget Analysis"])

    if options == "Home":
        display_home_page()
    elif options == "Budget Analysis":
        inputs = handle_inputs()
        if inputs and isinstance(inputs, UserDataInput):
            display_analysis_page(inputs)
            generate_advice_ui(inputs)

    # Set environment variable to resolve tokenizer warnings
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

if __name__ == "__main__":
    main()
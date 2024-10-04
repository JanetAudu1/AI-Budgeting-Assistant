import sys
from pathlib import Path
import os
import logging
import streamlit as st
import openai
from dotenv import load_dotenv

# Set page config as the first Streamlit command
st.set_page_config(page_title="AI Budgeting Assistant", page_icon="💰", layout="wide")

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

from app.ui.layout import display_home_page, display_analysis_page
from app.ui.input_handlers import handle_inputs
from app.ui.advice import generate_advice_ui
from app.api.models import UserDataInput
from app.services.recommender import generate_advice_stream

# Try to get the API key from Streamlit secrets, fall back to environment variable
try:
    # Access the OpenAI API key from the `api_keys` section in secrets
    openai.api_key = st.secrets["api_keys"]["OPENAI_API_KEY"]

except KeyError:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        st.error("OpenAI API key not found. Please set it in .streamlit/secrets.toml or as an environment variable.")
        st.stop()

# Similarly for HUGGINGFACE_TOKEN
try:
    os.environ["HUGGINGFACE_TOKEN"] = st.secrets["api_keys"]["HUGGINGFACE_TOKEN"]
except KeyError:
    if "HUGGINGFACE_TOKEN" not in os.environ:
        st.warning("Hugging Face token not found. Some features may not work.")


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
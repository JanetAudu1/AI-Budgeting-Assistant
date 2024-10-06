import sys
from pathlib import Path
import os
import logging
import streamlit as st
import openai
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables (this won't have an effect on Streamlit Cloud)
load_dotenv()

from app.ui.layout import display_home_page, display_analysis_page
from app.ui.input_handlers import handle_inputs
from app.ui.advice import generate_advice_ui
from app.api.models import UserDataInput
from app.services.recommender import generate_advice_stream

# Set page config as the first Streamlit command
st.set_page_config(page_title="AI Budgeting Assistant", page_icon="💰", layout="wide")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to check if running on Streamlit Cloud by checking the runtime environment
def is_streamlit_cloud() -> bool:
    """
    Detect if the app is running on Streamlit Cloud by checking the STREAMLIT_RUNTIME_ENV environment variable.
    """
    return os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud"

# Function to retrieve API keys from environment variables or Streamlit secrets
def get_api_key(key_name: str) -> str:
    """
    Retrieve the API key from Streamlit secrets (for cloud) or environment variables (for local development).
    """
    if is_streamlit_cloud():
        # Running on Streamlit Cloud, use secrets
        try:
            api_key = st.secrets["api_keys"].get(key_name)
            if api_key:
                logger.info(f"{key_name} found in Streamlit secrets.")
                return api_key
            else:
                logger.error(f"{key_name} not found in Streamlit secrets.")
        except Exception as e:
            logger.error(f"Error accessing Streamlit secrets: {str(e)}")
    else:
        # Running locally, use environment variables
        api_key = os.getenv(key_name)
        if api_key:
            logger.info(f"{key_name} found in environment variables.")
            return api_key
        else:
            logger.error(f"{key_name} not found in environment variables.")

    return None

# Set API keys
openai_api_key = get_api_key("OPENAI_API_KEY")
huggingface_token = get_api_key("HUGGINGFACE_TOKEN")

# Set OpenAI API key
if openai_api_key:
    openai.api_key = openai_api_key
    logger.info("OpenAI API key is set successfully.")
else:
    logger.error("OpenAI API key is not set.")

# Set Hugging Face token
if huggingface_token:
    logger.info("Hugging Face token is set successfully.")
else:
    logger.error("Hugging Face token is not set.")

def load_css():
    css_file = Path(__file__).parent.parent / "static" / "style.css"
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def apply_theme(theme):
    if theme == 'light':
        st.markdown("""
            <style>
            .stApp {
                background-color: white;
                color: black;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background-color: #0e1117;
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)

# Main function to run the Streamlit app
def main():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Theme toggle in sidebar
    if st.sidebar.checkbox("Use Light Theme", key='use_light_theme'):
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark'
    
    apply_theme(st.session_state.theme)
    
    # Main options in the sidebar
    options = st.sidebar.radio("Select a Section:", ["Home", "Budget Analysis"])

    if options == "Home":
        display_home_page()
    elif options == "Budget Analysis":
        if 'user_inputs' not in st.session_state:
            st.session_state.user_inputs = None

        inputs = handle_inputs()
        if inputs and isinstance(inputs, UserDataInput):
            st.session_state.user_inputs = inputs

        if st.session_state.user_inputs:
            display_analysis_page(st.session_state.user_inputs)
            generate_advice_ui(st.session_state.user_inputs)
        else:
            st.info("Please fill in your financial information to generate a budget analysis.")

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()


# Set environment variable to resolve tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
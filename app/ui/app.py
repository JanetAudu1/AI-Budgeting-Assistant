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

# Function to check if running on Streamlit Cloud
def is_streamlit_cloud() -> bool:
    return os.getenv("IS_STREAMLIT_CLOUD", "false").lower() == "true"

# Function to retrieve API keys
def get_api_key(key_name: str) -> str:
    if is_streamlit_cloud():
        # Import streamlit only when running on Streamlit Cloud
        import streamlit as st
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
        api_key = os.getenv(key_name)
        if api_key:
            logger.info(f"{key_name} found in environment variables.")
            return api_key
        else:
            logger.error(f"{key_name} not found in environment variables.")
    return None

# Debug: Print environment information
logger.info(f"Is Streamlit Cloud: {is_streamlit_cloud()}")
logger.info(f"STREAMLIT_RUNTIME_ENV: {os.getenv('STREAMLIT_RUNTIME_ENV')}")

# Set API keys
openai_api_key = get_api_key("OPENAI_API_KEY")
logger.info(f"Retrieved OpenAI API key: {'*****' if openai_api_key else 'None'}")

# Set OpenAI API key
if openai_api_key:
    openai.api_key = openai_api_key
    logger.info(f"OpenAI API key set: {'*****' if openai.api_key else 'None'}")
else:
    logger.error("OpenAI API key is not set.")

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

# Main function to run the Streamlit app
def main():

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
            
            # Double-check API key before making the call
            if not openai.api_key:
                openai.api_key = get_api_key("OPENAI_API_KEY")
                logger.info(f"Re-set OpenAI API key: {'*****' if openai.api_key else 'None'}")
            
            if not openai.api_key:
                st.error("OpenAI API key is not set. Please check your environment variables or Streamlit secrets configuration.")
                return
            
            generate_advice_ui(st.session_state.user_inputs)
        else:
            st.info("Please fill in your financial information to generate a budget analysis.")

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

# Set environment variable to resolve tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import sys
from pathlib import Path
import os
import logging
import streamlit as st
import openai
from dotenv import load_dotenv

# Check if running on Streamlit Cloud
is_streamlit_cloud = os.getenv('STREAMLIT_RUNTIME_ENV') == 'cloud'

# Print the result
print(f"Is Streamlit Cloud: {is_streamlit_cloud}")

# Set page config as the first Streamlit command
st.set_page_config(page_title="AI Budgeting Assistant", page_icon="💰", layout="wide")

# Configure logging to output to terminal
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

def get_api_key(key_name: str) -> str:
    # Check if running on Streamlit Cloud
    is_streamlit_cloud = os.getenv('STREAMLIT_RUNTIME_ENV') == 'cloud'
    logger.debug(f"Is Streamlit Cloud: {is_streamlit_cloud}")

    if not is_streamlit_cloud:
        # Print current working directory
        logger.debug(f"Current working directory: {os.getcwd()}")

        # Check if .env file exists
        env_path = Path('.env')
        if env_path.exists():
            logger.debug(f".env file found at {env_path.absolute()}")
            with open(env_path, 'r') as f:
                logger.debug(f".env file contents:\n{f.read()}")
        else:
            logger.error(f".env file not found in {env_path.absolute()}")

        # Load environment variables from .env file
        load_dotenv()

    api_key = os.getenv(key_name)
    if api_key:
        logger.debug(f"{key_name} found in environment variables")
    else:
        logger.error(f"{key_name} not found in environment variables")
    return api_key

# Set OpenAI API key
openai.api_key = get_api_key("OPENAI_API_KEY")

# Verify that the API key is set
if not openai.api_key:
    raise ValueError(f"OpenAI API key is not set. Please set the OPENAI_API_KEY in {'Streamlit secrets' if is_streamlit_cloud else 'environment variables'}.")
    
# Print whether the API key is set (don't print the actual key)
print(f"OpenAI API Key is set: {'Yes' if openai.api_key else 'No'}")

# Set Hugging Face token
huggingface_token = get_api_key("HUGGINGFACE_TOKEN")
if huggingface_token:
    os.environ["HUGGINGFACE_TOKEN"] = huggingface_token

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
    st.title("AI Budgeting Assistant")

    # Debug section (only visible when running locally)
    if not os.getenv('STREAMLIT_RUNTIME_ENV') == 'cloud':
        st.sidebar.header("Debug Information")
        if st.sidebar.checkbox("Show Environment Variables"):
            st.sidebar.subheader("Environment Variables")
            for key, value in os.environ.items():
                if key.startswith("OPENAI") or key in ["STREAMLIT_RUNTIME_ENV"]:
                    st.sidebar.text(f"{key}: {'*' * len(value)}")  # Mask the actual value
            
            # Specific check for OPENAI_API_KEY
            openai_key = os.getenv("OPENAI_API_KEY")
            st.sidebar.text(f"OPENAI_API_KEY set: {'Yes' if openai_key else 'No'}")
            
            # Check .env file
            if os.path.exists('.env'):
                st.sidebar.text(".env file exists")
                with open('.env', 'r') as f:
                    env_contents = f.read()
                st.sidebar.text("Contents of .env file (keys only):")
                for line in env_contents.split('\n'):
                    if '=' in line:
                        key = line.split('=')[0]
                        st.sidebar.text(f"  {key}: {'*' * 10}")
            else:
                st.sidebar.text(".env file not found")

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

    # Set environment variable to resolve tokenizer warnings
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

if __name__ == "__main__":
    main()
import sys
from pathlib import Path
import os
import logging
import streamlit as st
import openai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def is_streamlit_cloud():
    return os.getenv('STREAMLIT_RUNTIME_ENV') == 'cloud' or os.getenv('IS_STREAMLIT_CLOUD') == 'true'

def get_api_key(key_name: str) -> str:
    running_on_cloud = is_streamlit_cloud()
    logger.debug(f"Is Streamlit Cloud: {running_on_cloud}")
    
    if running_on_cloud:
        # Running on Streamlit Cloud, use secrets
        try:
            if "api_keys" in st.secrets:
                api_key = st.secrets["api_keys"].get(key_name)
                if api_key:
                    logger.debug(f"{key_name} found in Streamlit secrets")
                    return api_key
                else:
                    logger.warning(f"{key_name} not found in Streamlit secrets")
            else:
                logger.warning("'api_keys' section not found in Streamlit secrets")
        except Exception as e:
            logger.error(f"Error accessing Streamlit secrets: {str(e)}")
    else:
        # Running locally, use environment variables
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv(key_name)
        if api_key:
            logger.debug(f"{key_name} found in environment variables")
            return api_key
        else:
            logger.warning(f"{key_name} not found in environment variables")
    
    return None

# Set API keys
openai_api_key = get_api_key("OPENAI_API_KEY")
huggingface_token = get_api_key("HUGGINGFACE_TOKEN")

if openai_api_key:
    openai.api_key = openai_api_key
    os.environ["OPENAI_API_KEY"] = openai_api_key
    logger.info("OpenAI API key is set successfully.")
else:
    logger.error("OpenAI API key is not set.")

if huggingface_token:
    os.environ["HUGGINGFACE_TOKEN"] = huggingface_token
    logger.info("Hugging Face token is set successfully.")
else:
    logger.error("Hugging Face token is not set.")

from app.ui.layout import display_home_page, display_analysis_page
from app.ui.input_handlers import handle_inputs
from app.ui.advice import generate_advice_ui
from app.api.models import UserDataInput
from app.services.recommender import generate_advice_stream

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

            st.sidebar.text(f"Current working directory: {os.getcwd()}")

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
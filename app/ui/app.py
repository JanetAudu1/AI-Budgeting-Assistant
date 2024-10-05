import sys
from pathlib import Path
import os
import logging
import streamlit as st
import openai
from dotenv import load_dotenv

# Import your app's UI and logic modules
from app.ui.layout import display_home_page, display_analysis_page
from app.ui.input_handlers import handle_inputs
from app.ui.advice import generate_advice_ui
from app.api.models import UserDataInput
from app.services.recommender import generate_advice_stream

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to check if running on Streamlit Cloud
def is_streamlit_cloud() -> bool:
    """
    Detect if the app is running on Streamlit Cloud by checking the IS_STREAMLIT_CLOUD secret.
    """
    return st.secrets.get("IS_STREAMLIT_CLOUD", "false").lower() == "true"

# Function to retrieve API keys from secrets or environment variables
def get_api_key(key_name: str) -> str:
    """
    Retrieve the API key from either Streamlit secrets (in the cloud) or environment variables (locally).
    """
    if is_streamlit_cloud():
        # Running on Streamlit Cloud, use secrets
        try:
            api_key = st.secrets["api_keys"].get(key_name)
            if api_key:
                logger.debug(f"{key_name} found in Streamlit secrets")
                return api_key
            else:
                logger.warning(f"{key_name} not found in Streamlit secrets")
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

# Set OpenAI API key
if openai_api_key:
    openai.api_key = openai_api_key
    logger.info("OpenAI API key is set successfully.")
else:
    logger.error("OpenAI API key is not set.")

# Set Hugging Face token
if huggingface_token:
    os.environ["HUGGINGFACE_TOKEN"] = huggingface_token
    logger.info("Hugging Face token is set successfully.")
else:
    logger.error("Hugging Face token is not set.")

# Main function to run the Streamlit app
def main():
    st.title("AI Budgeting Assistant")

    # Debug section (visible when running locally)
    if not is_streamlit_cloud():
        st.sidebar.header("Debug Information")
        if st.sidebar.checkbox("Show Environment Variables"):
            st.sidebar.subheader("Environment Variables")
            for key, value in os.environ.items():
                if key.startswith("OPENAI") or key in ["STREAMLIT_RUNTIME_ENV"]:
                    st.sidebar.text(f"{key}: {'*' * len(value)}")  # Mask the actual value
            
            # Specific check for OPENAI_API_KEY
            openai_key = os.getenv("OPENAI_API_KEY")
            st.sidebar.text(f"OPENAI_API_KEY set: {'Yes' if openai_key else 'No'}")
            
            # Check .env file existence
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

    # Set environment variable to resolve tokenizer warnings
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

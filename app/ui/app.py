import os
import sys
import logging
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import streamlit as st
import openai

# Now import your app's UI and logic modules
from ui.layout import display_home_page, display_analysis_page
from ui.input_handlers import handle_inputs
from ui.advice import generate_advice_ui
from api.models import UserDataInput
from services.recommender import generate_advice_stream

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to check if running on Streamlit Cloud (via secrets)
def is_streamlit_cloud() -> bool:
    """
    Detect if the app is running on Streamlit Cloud by checking the IS_STREAMLIT_CLOUD secret.
    """
    return st.secrets.get("IS_STREAMLIT_CLOUD", "false").lower() == "true"

# Function to retrieve API keys from Streamlit secrets
def get_api_key(key_name: str) -> str:
    """
    Retrieve the API key from Streamlit secrets.
    """
    try:
        api_key = st.secrets["api_keys"].get(key_name)
        if api_key:
            logger.debug(f"{key_name} found in Streamlit secrets.")
            return api_key
        else:
            logger.error(f"{key_name} not found in Streamlit secrets.")
    except Exception as e:
        logger.error(f"Error accessing Streamlit secrets: {str(e)}")
    
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

# Main function to run the Streamlit app
def main():
    st.title("AI Budgeting Assistant")

    # Debug: Print session state
    st.write("Session State:", st.session_state)

    # Main options in the sidebar
    options = st.sidebar.radio("Select a Section:", ["Home", "Budget Analysis"])

    if options == "Home":
        display_home_page()
    elif options == "Budget Analysis":
        st.write("Debug: Entered Budget Analysis section")
        
        if 'user_inputs' not in st.session_state:
            st.session_state.user_inputs = None

        inputs = handle_inputs()
        st.write("Debug: Inputs received:", inputs)

        if inputs and isinstance(inputs, UserDataInput):
            st.session_state.user_inputs = inputs
            st.write("Debug: User inputs set in session state")

            st.write("Debug: Displaying analysis")
            display_analysis_page(st.session_state.user_inputs)
            generate_advice_ui(st.session_state.user_inputs)
        else:
            st.info("Please fill in your financial information to generate a budget analysis.")

        # Debug: Print final session state
        st.write("Final Session State:", st.session_state)

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

# Set environment variable to resolve tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

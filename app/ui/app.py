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

def get_api_key(key_name: str) -> str:
    # Check if running on Streamlit Cloud
    is_streamlit_cloud = os.getenv('STREAMLIT_RUNTIME_ENV') == 'cloud'
    logger.debug(f"Is Streamlit Cloud: {is_streamlit_cloud}")
    
    if not is_streamlit_cloud:
        # Running locally, use environment variables
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv(key_name)
        if api_key:
            logger.debug(f"{key_name} found in environment variables")
        else:
            logger.warning(f"{key_name} not found in environment variables")
    else:
        # Running on Streamlit Cloud, use secrets
        try:
            api_key = st.secrets["api_keys"][key_name]
            logger.debug(f"{key_name} found in Streamlit secrets")
        except KeyError:
            logger.warning(f"{key_name} not found in Streamlit secrets")
            api_key = None
    
    return api_key

# Set OpenAI API key
api_key = get_api_key("OPENAI_API_KEY")
if api_key:
    openai.api_key = api_key
    os.environ["OPENAI_API_KEY"] = api_key  # Set environment variable for other parts of the app
    logger.info("OpenAI API key is set successfully.")
else:
    logger.error("OpenAI API key is not set.")

def main():
    st.title("AI Budgeting Assistant")

    # Debug section
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

    # Rest of your Streamlit app code...
    if not openai.api_key:
        st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY in environment variables (local) or Streamlit secrets (cloud).")
    else:
        # Your app logic here
        pass

if __name__ == "__main__":
    main()
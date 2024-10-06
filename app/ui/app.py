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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# At the very beginning of your app
st.set_page_config(
    page_title="AI Budgeting Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define light and dark theme CSS
light_theme = """
<style>
    .stApp {background-color: #FFFFFF; color: #000000;}
    .stButton>button {background-color: #3D9970; color: white;}
    .stTextArea>div>div>textarea {background-color: #F0F2F6; color: #000000;}
    .streamlit-expanderHeader {font-size: 16px; font-weight: bold; color: #000000;}
</style>
"""

dark_theme = """
<style>
    /* Main app background */
    .stApp {background-color: #0E1117; color: #FFFFFF;}
    
    /* Header */
    .stApp > header {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    /* All text in sidebar */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stCheckbox,
    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSelectbox"],
    [data-testid="stSidebar"] .stSlider {
        color: #FFFFFF !important;
    }
    
    /* Buttons */
    .stButton>button {background-color: #3D9970; color: white;}
    
    /* Text areas, input fields, and their labels */
    .stTextArea>div>div>textarea,
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }
    
    /* Labels for all form inputs */
    .stTextArea label,
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stFileUploader label,
    .stDateInput label {
        color: #FFFFFF !important;
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: #262730;
        color: #FFFFFF !important;
    }
    
    /* Headers, subheaders, and all text elements */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #FFFFFF !important;
    }
    
    /* Ensure all text inputs and their labels are white */
    .stTextInput, .stTextInput>div>div>input::placeholder {
        color: #FFFFFF !important;
    }
    
    /* Date input fields */
    .stDateInput>div>div>input {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }
    
    /* Specific text elements */
    [data-testid="stText"] {
        color: #FFFFFF !important;
    }
    
    /* Financial analysis results */
    .element-container, .stDataFrame {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }
    
    /* Table headers and cells */
    .dataframe th, .dataframe td {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }
    
    /* Metric elements */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
    }
    
    /* Expander elements */
    .streamlit-expanderHeader {
        background-color: #262730 !important;
        color: #FFFFFF !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
    }
    
    /* Specific elements */
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stFileUploader"] label,
    .stMarkdown a {
        color: #FFFFFF !important;
    }
</style>
"""

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

# Main function to run the Streamlit app
def main():
    # Theme toggle in sidebar
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    if st.sidebar.checkbox("Use Light Theme", key='use_light_theme'):
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark'
    
    # Apply the selected theme
    if st.session_state.theme == 'light':
        st.markdown(light_theme, unsafe_allow_html=True)
    else:
        st.markdown(dark_theme, unsafe_allow_html=True)

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

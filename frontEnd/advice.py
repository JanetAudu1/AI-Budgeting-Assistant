import logging
import requests
import json
from backEnd.data_validation import UserData
import streamlit as st

logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000"  # Adjust this if your FastAPI server runs on a different port

def generate_advice_ui(inputs: UserData):
    """
    Generate and display financial advice in the Streamlit UI.

    Args:
        inputs (UserData): The user's financial data and goals.
    """
    advice_placeholder = st.empty()
    complete_advice = ""

    try:
        # Convert UserData to dictionary
        user_data_dict = inputs.to_dict()
        
        # Ensure the data is JSON serializable
        json_data = json.dumps(user_data_dict)
        
        # Make a POST request to the FastAPI endpoint with streaming enabled
        with requests.post(f"{API_URL}/get_advice", data=json_data, headers={'Content-Type': 'application/json'}, stream=True) as response:
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        complete_advice += chunk
                        advice_placeholder.text(complete_advice)
            else:
                st.error(f"Failed to get advice. Status code: {response.status_code}")
                logger.error(f"API error: {response.text}")
    
    except requests.RequestException as e:
        st.error("Failed to connect to the advice service.")
        logger.error(f"Request error: {str(e)}")
    except json.JSONDecodeError as e:
        st.error("Error in data serialization.")
        logger.error(f"JSON encode error: {str(e)}")
    except Exception as e:
        st.error("An unexpected error occurred.")
        logger.error(f"Unexpected error: {str(e)}")

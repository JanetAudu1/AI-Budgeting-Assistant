import logging
import requests
import json
import re
from backEnd.data_validation import UserData
import streamlit as st
import pandas as pd
import io

logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000" 

def clean_text(text):
    # Preserve line breaks, remove extra whitespace
    lines = text.split('\n')
    cleaned_lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]
    # Remove empty lines
    cleaned_lines = [line for line in cleaned_lines if line]
    return '\n\n'.join(cleaned_lines)  # Join with double newlines for better readability

def escape_dollar_signs(text):
    return text.replace('$', r'\$')

def generate_advice_ui(inputs: UserData):
    """
    Generate and display financial advice in the Streamlit UI.

    Args:
        inputs (UserData): The user's financial data and goals.
    """
    st.markdown("""
    <style>
    .advice-container {
        white-space: pre-wrap;
        overflow-wrap: break-word;
        word-wrap: break-word;
        hyphens: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Financial Advice")
    
    advice_placeholder = st.empty()
    
    try:
        # Convert UserData to dictionary
        user_data_dict = inputs.to_dict()
        
        # Ensure the data is JSON serializable
        json_data = json.dumps(user_data_dict)
        
        # Make a POST request to the FastAPI endpoint with streaming enabled
        with requests.post(f"{API_URL}/get_advice", data=json_data, headers={'Content-Type': 'application/json'}, stream=True) as response:
            if response.status_code == 200:
                complete_advice = ""
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        complete_advice += chunk
                        # Display everything up to the budget JSON marker
                        display_text = complete_advice.split("---BUDGET_JSON_START---")[0]
                        advice_placeholder.markdown(escape_dollar_signs(clean_text(display_text)))
        
                # After streaming, handle the budget JSON
                parts = complete_advice.split("---BUDGET_JSON_START---")
                if len(parts) > 1:
                    budget_json_part = parts[1].split("---BUDGET_JSON_END---")[0]
                    
                    try:
                        budget_json = json.loads(budget_json_part)
                        budget_data = budget_json["Proposed Monthly Budget"]
                        
                        # Create DataFrame from budget data
                        df = pd.DataFrame(list(budget_data.items()), columns=['Category', 'Amount'])
                        df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}")
                        
                        st.markdown("## 📊 Proposed Monthly Budget")
                        st.table(df)
                        
                        # Allow user to download the budget as CSV
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download Budget as CSV",
                            data=csv,
                            file_name="proposed_monthly_budget.csv",
                            mime="text/csv",
                        )
                    except json.JSONDecodeError:
                        st.write("Error parsing budget data.")
                else:
                    st.write("No budget data found in the advice.")

                # Display the conclusion
                conclusion = re.search(r"Best of luck with your financial journey,.*", complete_advice)
                if conclusion:
                    st.markdown(escape_dollar_signs(conclusion.group()))

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
        st.error(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")

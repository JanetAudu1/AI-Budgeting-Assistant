import json
import re
import pandas as pd
import streamlit as st
from app.api.models import UserDataInput  
import logging
import requests

logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000" 

def escape_dollar_signs(text):
    return text.replace('$', r'\$')

def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]
    cleaned_lines = [line for line in cleaned_lines if line]
    return '\n\n'.join(cleaned_lines)

def extract_budget_json(complete_advice):
    parts = complete_advice.split("---BUDGET_JSON_START---")
    if len(parts) > 1:
        budget_json_part = parts[1].split("---BUDGET_JSON_END---")[0]
        try:
            return json.loads(budget_json_part)
        except json.JSONDecodeError:
            st.write("Error parsing budget data.")
    return None

def create_budget_dataframe(budget_data):
    df = pd.DataFrame(list(budget_data.items()), columns=['Category', 'Amount'])
    df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}")
    return df

def display_budget_table(df):
    st.markdown("## 📊 Proposed Monthly Budget")
    st.table(df)

def create_budget_download(df):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Budget as CSV",
        data=csv,
        file_name="proposed_monthly_budget.csv",
        mime="text/csv",
    )

def display_conclusion(complete_advice):
    conclusion = re.search(r"I'm excited to support you.*", complete_advice)
    if conclusion:
        st.markdown(escape_dollar_signs(conclusion.group()))

def generate_advice_ui(inputs: UserDataInput):
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

    st.subheader("FinancialAnalysis and Proposed Budget")
    
    advice_placeholder = st.empty()
    
    try:
        json_data = inputs.model_dump_json()
        
        with st.spinner("Generating personalized financial analysis and proposed budget..."):
            response = requests.post(f"{API_URL}/get_advice", data=json_data, headers={'Content-Type': 'application/json'}, stream=True)
            
            if response.status_code == 200:
                complete_advice = ""
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        complete_advice += chunk
                        display_text = complete_advice.split("---BUDGET_JSON_START---")[0]
                        advice_placeholder.markdown(escape_dollar_signs(clean_text(display_text)))
                
                budget_json = extract_budget_json(complete_advice)
                if budget_json:
                    budget_data = budget_json.get("Proposed Monthly Budget")
                    if budget_data:
                        df = create_budget_dataframe(budget_data)
                        display_budget_table(df)
                        create_budget_download(df)
                    else:
                        st.warning("No budget data found in the advice.")
                else:
                    st.warning("No budget data found in the advice.")

                display_conclusion(complete_advice)
            else:
                st.error(f"Failed to get advice. Status code: {response.status_code}")
                st.error(f"Response content: {response.text}")

    except requests.RequestException as e:
        st.error(f"Failed to connect to the advice service: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
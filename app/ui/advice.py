import json
import re
import pandas as pd
import streamlit as st
from app.api.models import UserDataInput  
import logging
import requests
import traceback

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

def create_budget_dataframe(budget_data, bank_statement, current_income):
    if not isinstance(budget_data, dict):
        st.warning("Invalid budget data format. Expected a dictionary.")
        return pd.DataFrame()

    previous_spend = bank_statement.groupby('Category')['Withdrawals'].sum().to_dict()

    rows = []
    total_proposed = 0
    for category, data in budget_data.items():
        if category.lower() not in ['income', 'deposits', 'paychecks']:
            prev_spend = previous_spend.get(category, 0)
            
            if isinstance(data, dict):
                proposed_change = data.get('proposed_change', prev_spend)
                change_reason = data.get('change_reason', '')
            else:
                proposed_change = data
                change_reason = ''

            if isinstance(proposed_change, str):
                proposed_change = float(proposed_change.replace('$', '').replace(',', ''))
            
            difference = proposed_change - prev_spend
            percentage_change = (difference / prev_spend * 100) if prev_spend != 0 else 100

            # Provide a default explanation for significant changes if no reason is given
            if not change_reason and abs(percentage_change) > 10:
                if difference < 0:
                    change_reason = f"Significant decrease of {abs(percentage_change):.2f}% suggested to optimize budget."
                else:
                    change_reason = f"Increase of {percentage_change:.2f}% suggested based on financial goals and priorities."

            total_proposed += proposed_change
            
            rows.append({
                'Category': category,
                'Previous Spend': prev_spend,
                'Proposed Change': proposed_change,
                'Difference': difference,
                'Change Reason': change_reason
            })

    # Adjust proposed changes if they exceed current income
    if total_proposed > current_income:
        adjustment_factor = current_income / total_proposed
        for row in rows:
            row['Proposed Change'] *= adjustment_factor
            row['Difference'] = row['Proposed Change'] - row['Previous Spend']
        total_proposed = current_income

    # Add savings category if not present
    if 'Savings' not in [row['Category'] for row in rows]:
        savings_amount = current_income - total_proposed
        rows.append({
            'Category': 'Savings',
            'Previous Spend': previous_spend.get('Savings', 0),
            'Proposed Change': savings_amount,
            'Difference': savings_amount - previous_spend.get('Savings', 0),
            'Change Reason': 'Allocated remaining amount to savings'
        })

    df = pd.DataFrame(rows)

    if df.empty:
        st.warning("No valid budget data available to display.")
        return df

    for col in ['Previous Spend', 'Proposed Change', 'Difference']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.sort_values('Difference', key=abs, ascending=False).reset_index(drop=True)

    for col in ['Previous Spend', 'Proposed Change', 'Difference']:
        df[col] = df[col].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "$0.00")

    return df

def display_budget_table(df, current_income):
    st.markdown("## 📊 Proposed Monthly Budget")
    
    if df.empty:
        st.warning("No budget data available to display.")
        return

    st.table(df)
    
    try:
        total_previous = df['Previous Spend'].replace('[\$,]', '', regex=True).astype(float).sum()
        total_proposed = df['Proposed Change'].replace('[\$,]', '', regex=True).astype(float).sum()
        
        st.markdown(escape_dollar_signs(f"**Total Monthly Income:** ${current_income:,.2f}"))
        st.markdown(escape_dollar_signs(f"**Total Previous Spend:** ${total_previous:,.2f}"))
        st.markdown(escape_dollar_signs(f"**Total Proposed Spend:** ${total_proposed:,.2f}"))
        
        if abs(total_proposed - current_income) < 0.01:
            st.success("✅ The proposed budget matches the monthly income.")
        else:
            st.error(escape_dollar_signs(f"⚠️ The proposed budget (${total_proposed:,.2f}) does not match the monthly income (${current_income:,.2f})."))
    except Exception as e:
        st.warning(f"Unable to calculate totals: {str(e)}")

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

    st.subheader("Financial Analysis and Proposed Budget")
    
    advice_placeholder = st.empty()
    
    try:
        json_data = inputs.model_dump_json()
        
        with st.spinner("Generating personalized financial analysis and proposed budget..."):
            response = requests.post(
                f"{API_URL}/get_advice", 
                data=json_data, 
                headers={'Content-Type': 'application/json'}, 
                stream=True
            )
            
            if response.status_code == 200:
                complete_advice = ""
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        complete_advice += chunk
                        display_text = complete_advice.split("---BUDGET_JSON_START---")[0]
                        advice_placeholder.markdown(escape_dollar_signs(clean_text(display_text)))
                
                budget_json = extract_budget_json(complete_advice)
                if budget_json:
                    # Flatten the budget data if it's nested
                    budget_data = budget_json.get("Proposed Monthly Budget", budget_json)
                    if isinstance(budget_data, dict):

                        # Convert bank_statement to DataFrame if it's not already
                        bank_statement = pd.DataFrame([entry.dict() for entry in inputs.bank_statement])
                        df = create_budget_dataframe(budget_data, bank_statement, inputs.current_income)
                        if not df.empty:
                            display_budget_table(df, inputs.current_income)  # Use current_income here
                            create_budget_download(df)
                        else:
                            st.warning("Unable to create budget table from the provided data.")
                    else:
                        st.warning("Invalid budget data structure.")
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
        st.error(f"Traceback: {traceback.format_exc()}")  # Add this line for more detailed error information
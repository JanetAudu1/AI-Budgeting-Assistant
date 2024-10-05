import json
import re
import pandas as pd
import streamlit as st
from app.api.models import UserDataInput  
import logging
from app.services.recommender import generate_advice_stream

logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000" #not in use, as main.py is not running. Removed for easier deployment 

def escape_dollar_signs(text):
    return text.replace('$', r'\$')

def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]
    cleaned_lines = [line for line in cleaned_lines if line]
    return '\n\n'.join(cleaned_lines)

def extract_budget_json(complete_advice):
    start_marker = "---BUDGET_JSON_START---"
    end_marker = "---BUDGET_JSON_END---"
    
    try:
        start_index = complete_advice.index(start_marker) + len(start_marker)
        end_index = complete_advice.index(end_marker, start_index)
        budget_json_part = complete_advice[start_index:end_index].strip()
        
        try:
            budget_data = json.loads(budget_json_part)
            if "Proposed Monthly Budget" in budget_data:
                return budget_data["Proposed Monthly Budget"]
            else:
                return budget_data
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing budget JSON: {e}")
            logger.debug(f"Attempted to parse: {budget_json_part}")
            return None
    except ValueError:
        logger.warning("Budget JSON markers not found in the advice")
        return None

def create_budget_dataframe(budget_data, bank_statement, current_income):
    if not isinstance(budget_data, dict):
        st.warning("Invalid budget data format. Expected a dictionary.")
        return pd.DataFrame()

    # Convert bank_statement to DataFrame if it's a list
    if isinstance(bank_statement, list):
        bank_statement = pd.DataFrame(bank_statement)

    # Check if 'Category' column exists, if not, use a default category
    if 'Category' not in bank_statement.columns:
        st.warning("'Category' column not found in bank statement. Using 'Uncategorized' for all entries.")
        bank_statement['Category'] = 'Uncategorized'

    # Check if 'Withdrawals' column exists, if not, use 'Amount' or create a default
    if 'Withdrawals' not in bank_statement.columns:
        if 'Amount' in bank_statement.columns:
            bank_statement['Withdrawals'] = bank_statement['Amount'].apply(lambda x: abs(float(x)) if x < 0 else 0)
        else:
            st.warning("'Withdrawals' or 'Amount' column not found. Using 0 for all entries.")
            bank_statement['Withdrawals'] = 0

    previous_spend = bank_statement.groupby('Category')['Withdrawals'].sum().to_dict()

    rows = []
    total_proposed = 0
    for category, details in budget_data.items():
        if isinstance(details, dict):
            try:
                proposed_change = float(details.get('proposed_change', 0))
            except ValueError:
                st.warning(f"Invalid proposed change for {category}. Using 0.")
                proposed_change = 0
            change_reason = details.get('change_reason', '')
        elif isinstance(details, (int, float)):
            proposed_change = float(details)
            change_reason = ''
        else:
            st.warning(f"Invalid data for {category}. Skipping this category.")
            continue

        previous = float(previous_spend.get(category, 0))
        
        # Calculate the new proposed amount
        new_amount = previous + proposed_change
        
        # Calculate percentage change
        if previous != 0:
            percent_change = ((new_amount - previous) / previous) * 100
        else:
            percent_change = float('inf') if new_amount > 0 else 0
        
        rows.append({
            'Category': category,
            'Previous Spend': previous,
            'Proposed Change': new_amount,
            'Percent Change': percent_change,
            'Change Reason': change_reason
        })
        total_proposed += new_amount

    # Adjust proposed changes if they exceed current income
    if total_proposed > current_income:
        adjustment_factor = current_income / total_proposed
        for row in rows:
            row['Proposed Change'] *= adjustment_factor
            row['Percent Change'] = ((row['Proposed Change'] - row['Previous Spend']) / row['Previous Spend']) * 100 if row['Previous Spend'] != 0 else float('inf')

    # Add savings category if not present
    if 'Savings' not in [row['Category'] for row in rows]:
        savings_amount = current_income - sum(row['Proposed Change'] for row in rows)
        previous_savings = float(previous_spend.get('Savings', 0))
        percent_change = ((savings_amount - previous_savings) / previous_savings) * 100 if previous_savings != 0 else float('inf')
        rows.append({
            'Category': 'Savings',
            'Previous Spend': previous_savings,
            'Proposed Change': savings_amount,
            'Percent Change': percent_change,
            'Change Reason': 'Allocated remaining amount to savings'
        })

    df = pd.DataFrame(rows)

    if df.empty:
        st.warning("No valid budget data available to display.")
        return df

    for col in ['Previous Spend', 'Proposed Change']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.sort_values('Percent Change', key=abs, ascending=False).reset_index(drop=True)

    for col in ['Previous Spend', 'Proposed Change']:
        df[col] = df[col].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "$0.00")
    
    df['Percent Change'] = df['Percent Change'].apply(lambda x: f"{x:,.2f}%" if pd.notnull(x) else "N/A")

    return df

def display_budget_table(df, current_income):
    st.subheader(f"Proposed Monthly Budget (Total Income: ${current_income:.2f})")
    
    # Calculate total proposed spend
    total_proposed = df['Proposed Change'].apply(lambda x: float(x.replace('$', '').replace(',', ''))).sum()
    
    # Display the table
    st.table(df[['Category', 'Previous Spend', 'Proposed Change', 'Percent Change', 'Change Reason']])
    
    # Display total proposed spend
    st.write(f"Total Proposed Spend: ${total_proposed:.2f}")
    
    # Calculate and display remaining budget
    remaining_budget = current_income - total_proposed
    st.write(f"Remaining Budget: ${remaining_budget:.2f}")

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
    st.subheader("Financial Analysis and Proposed Budget")
    
    # Initialize session state
    if 'regenerate' not in st.session_state:
        st.session_state.regenerate = False
    if 'regenerated_once' not in st.session_state:
        st.session_state.regenerated_once = False
    if 'follow_up_question' not in st.session_state:
        st.session_state.follow_up_question = ""
    if 'analysis_generated' not in st.session_state:
        st.session_state.analysis_generated = False

    advice_placeholder = st.empty()
    budget_placeholder = st.empty()
    
    try:
        # Generate or display advice
        if not st.session_state.analysis_generated or st.session_state.regenerate:
            complete_advice = ""
            
            # Acknowledge the follow-up question if it exists
            if st.session_state.follow_up_question:
                st.info(f"Regenerating analysis based on your follow-up: '{st.session_state.follow_up_question}'")
            
            with st.spinner("Generating personalized financial analysis and proposed budget..."):
                for chunk in generate_advice_stream(inputs, st.session_state.follow_up_question):
                    complete_advice += chunk
                    display_text = complete_advice.split("---BUDGET_JSON_START---")[0]
                    
                    # Insert Budgeting Constraints after Financial Goals
                    goals_index = display_text.find("Financial Goals:")
                    if goals_index != -1:
                        next_section_index = display_text.find("\n\n", goals_index)
                        if next_section_index != -1:
                            constraints_text = "\n\nBudgeting Constraints:\n"
                            for constraint in inputs.constraints:
                                constraints_text += f"• {constraint}\n"
                            display_text = display_text[:next_section_index] + constraints_text + display_text[next_section_index:]
                    
                    advice_placeholder.markdown(escape_dollar_signs(clean_text(display_text)))
            
            st.session_state.complete_advice = complete_advice
            st.session_state.regenerate = False
            st.session_state.analysis_generated = True
        else:
            complete_advice = st.session_state.complete_advice
            display_text = complete_advice.split("---BUDGET_JSON_START---")[0]
            
            # Insert Budgeting Constraints after Financial Goals
            goals_index = display_text.find("Financial Goals:")
            if goals_index != -1:
                next_section_index = display_text.find("\n\n", goals_index)
                if next_section_index != -1:
                    constraints_text = "\n\nBudgeting Constraints:\n"
                    for constraint in inputs.constraints:
                        constraints_text += f"• {constraint}\n"
                    display_text = display_text[:next_section_index] + constraints_text + display_text[next_section_index:]
            
            advice_placeholder.markdown(escape_dollar_signs(clean_text(display_text)))

        # Display budget
        budget_data = extract_budget_json(complete_advice)
        if budget_data:
            budget_data = budget_data.get("Proposed Monthly Budget", budget_data)
            if isinstance(budget_data, dict):
                bank_statement = pd.DataFrame([entry.dict() for entry in inputs.bank_statement])
                df = create_budget_dataframe(budget_data, bank_statement, inputs.current_income)
                if not df.empty:
                    budget_placeholder.empty()
                    with budget_placeholder.container():
                        if st.session_state.regenerated_once:
                            st.subheader("Updated Proposed Budget")
                        else:
                            st.subheader("Proposed Budget")
                        display_budget_table(df, inputs.current_income)
                        create_budget_download(df)
                else:
                    st.warning("Unable to create budget table from the provided data.")
            else:
                st.warning("Invalid budget data structure.")
        else:
            st.warning("No budget data found in the advice. This might be due to an incomplete AI response or formatting issue.")
            logger.warning(f"Complete advice without budget data: {complete_advice}")
        
        display_conclusion(complete_advice)

        # Follow-up question input
        st.subheader("Have a follow-up question or comment?")
        follow_up_question = st.text_area("Enter your question or comment here:", 
                                          value=st.session_state.follow_up_question,
                                          height=100,
                                          max_chars=500)
        
        # Save the follow-up question in session state
        st.session_state.follow_up_question = follow_up_question

        # Regenerate button
        if not st.session_state.regenerated_once:
            if st.button("Regenerate Analysis"):
                st.session_state.regenerate = True
                st.session_state.regenerated_once = True
                st.session_state.analysis_generated = False
                st.experimental_rerun()
        else:
            st.warning("You've already regenerated the analysis once. To get a new analysis, please start over with new inputs.")
            if st.button("Start Over"):
                # Clear all session state variables
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.exception(e)
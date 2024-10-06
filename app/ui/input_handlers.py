import sys
from pathlib import Path
import pandas as pd
import streamlit as st
from pydantic import ValidationError
from datetime import date

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.api import models

def handle_inputs():
    """
    Handle user input for financial data and create a UserDataInput object.

    This function manages the UI for user input, including file uploads for bank statements
    and form inputs for personal financial information. It processes the inputs and
    creates a UserDataInput object if all required data is provided.

    Returns:
        UserDataInput: A UserDataInput object containing the user's financial data,
                       or None if the input is incomplete or invalid.
    """
    st.subheader("📝 Enter Your Financial Information")
    
    uploaded_file = st.file_uploader("Upload your bank statement (CSV format)", type="csv")
    
    if uploaded_file is None:
        st.warning("Please upload your bank statement.")
        return None

    df = pd.read_csv(uploaded_file)
    st.write("Bank statement uploaded successfully!")
    
    for col in ['Withdrawals', 'Deposits', 'Balance']:
        if col in df.columns:
            df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
            
    st.subheader("Bank Statement Preview")
    st.write(df.head())

    name = st.text_input("Name", max_chars=100)
    age = st.number_input("Age", min_value=18, max_value=120, step=1)
    address = st.text_input("Address (State)", help="Please enter your state of residence")
    current_income = st.number_input("Current Net Monthly Income ($)", min_value=0.0, step=100.0, format="%.2f")
    current_savings = st.number_input("Current Savings ($)", min_value=0.0, step=1000.0, format="%.2f")
    goals = st.text_area("Financial Goals (comma-separated)", max_chars=500)
    timeline_months = st.number_input("Timeline (months)", min_value=1, max_value=600, step=1)

    constraints = st.text_area("Budgeting Constraints (One per line, optional)", help="Enter any specific constraints you want to be considered in your budget analysis.")
    constraints_list = [constraint.strip() for constraint in constraints.split('\n') if constraint.strip()]

    llm_options = ["GPT-4 (Default)", "distilgpt2", "gpt2"]
    selected_llm = st.selectbox("Select LLM Model", llm_options)

    if st.button("Generate Analysis"):
        try:
            goals_list = [goal.strip() for goal in goals.split(',') if goal.strip()]
            
            bank_statement_entries = [
                models.BankStatementEntry(
                    Date=pd.to_datetime(row['Date']).date(),
                    Description=row['Description'],
                    Category=row['Category'],
                    Withdrawals=float(row.get('Withdrawals', 0)),
                    Deposits=float(row.get('Deposits', 0))
                ) for _, row in df.iterrows()
            ]

            # Remove "(Default)" from the selected model name if present
            selected_model = selected_llm.split(" ")[0] if "(Default)" in selected_llm else selected_llm

            user_data = models.UserDataInput(
                name=name,
                age=age,
                state=address,  
                current_income=current_income,
                current_savings=current_savings,
                goals=goals_list,
                timeline_months=timeline_months,
                bank_statement=bank_statement_entries,
                selected_llm=selected_model, 
                constraints=constraints_list
            )
            return user_data
        except ValidationError as ve:
            for error in ve.errors():
                st.error(f"{error['loc'][0]}: {error['msg']}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    
    return None
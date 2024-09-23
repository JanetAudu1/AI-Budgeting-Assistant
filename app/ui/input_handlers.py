import sys
from pathlib import Path
import pandas as pd
from typing import Dict
import streamlit as st

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.data_validation import UserData

def calculate_expenses(bank_statement: pd.DataFrame) -> Dict[str, float]:
    # Ensure 'Withdrawals' column exists and is numeric
    if 'Withdrawals' not in bank_statement.columns:
        raise ValueError("Bank statement must have a 'Withdrawals' column")
    
    bank_statement['Withdrawals'] = pd.to_numeric(bank_statement['Withdrawals'], errors='coerce')

    # Group by category and sum withdrawals
    expenses = bank_statement.groupby('Category')['Withdrawals'].sum()

    # Convert to dictionary
    categorized_expenses = expenses.to_dict()

    return categorized_expenses

def handle_inputs():
    st.subheader("📝 Enter Your Financial Information")
    
    # File uploader for bank statement
    uploaded_file = st.file_uploader("Upload your bank statement (CSV format)", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Bank statement uploaded successfully!")
        
        # Clean 'Withdrawals' column if necessary
        df['Withdrawals'] = df['Withdrawals'].replace('[\$,]', '', regex=True).astype(float)
        
        # Calculate expenses
        categorized_expenses = calculate_expenses(df)

    else:
        st.warning("Please upload your bank statement.")
        return None

    name = st.text_input("Name", max_chars=100)
    age = st.number_input("Age", min_value=18, max_value=120, step=1)
    address = st.text_input("Address", max_chars=200)
    current_income = st.number_input("Current Net Monthly Income ($)", min_value=0.0, step=100.0, format="%.2f")
    current_savings = st.number_input("Current Savings ($)", min_value=0.0, step=1000.0, format="%.2f")
    goals = st.text_area("Financial Goals (comma-separated)", max_chars=500)
    timeline_months = st.number_input("Timeline (months)", min_value=1, max_value=600, step=1)

    if st.button("Generate Analysis"):
        try:
            user_data = UserData(
                name=name,
                age=age,
                address=address,
                current_income=current_income,
                current_savings=current_savings,
                goals=[goal.strip() for goal in goals.split(',') if goal.strip()],
                timeline_months=timeline_months,
                bank_statement=df
            )
            
            if user_data.validate() and user_data.validate_bank_statement():
                return user_data
            else:
                for error in user_data.validation_errors:
                    st.error(error)
                return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    return None

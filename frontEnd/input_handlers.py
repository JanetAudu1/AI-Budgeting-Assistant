import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backEnd.data_validation import UserData
import streamlit as st
import pandas as pd

def handle_inputs():
    st.subheader("📝 Enter Your Financial Information")
    
    # File uploader for bank statement
    uploaded_file = st.file_uploader("Upload your bank statement (CSV format)", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Bank statement uploaded successfully!")
    else:
        st.write("Please upload your bank statement.")
        return None

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    address = st.text_input("Address")
    current_income = st.number_input("Current Monthly Income ($)", min_value=0.0, format="%.2f")
    current_savings = st.number_input("Current Savings ($)", min_value=0.0, format="%.2f")
    goals = st.text_area("Financial Goals (comma-separated)")
    timeline_months = st.number_input("Timeline (months)", min_value=1, step=1)
    priorities = st.text_area("Priorities (comma-separated)")
    savings_goal = st.number_input("Savings Goal ($)", min_value=0.0, format="%.2f")

    if st.button("Generate Analysis"):
        user_data = UserData(
            name=name,
            age=age,
            address=address,
            current_income=current_income,
            current_savings=current_savings,
            goals=[goal.strip() for goal in goals.split(',')],
            timeline_months=timeline_months,
            bank_statement=df,
            priorities=[priority.strip() for priority in priorities.split(',')],
            savings_goal=savings_goal
        )
        return user_data
    return None

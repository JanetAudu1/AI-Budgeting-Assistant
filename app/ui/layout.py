import streamlit as st
import pandas as pd
from app.ui.charts import (
    generate_expense_chart,
    generate_income_vs_expenses_chart,
    generate_savings_projection
)
from app.api.models import UserDataInput
from app.ui.advice import escape_dollar_signs

def display_sample_bank_statement():
    sample_data = {
        'Date': ['9/1/2024', '9/5/2024', '9/10/2024', '9/15/2024', '9/16/2024'],
        'Description': ['Paycheck', 'Rent Payment', 'Groceries', 'Utilities', 'Coffee'],
        'Debit': ['', 1000, 300, 200, 100],
        'Credit': [3500, '', '', '', ''],
        'Category': ['Income', 'Rent', 'Groceries', 'Utilities', 'Personal'],
        'Balance': [3500, 2500, 2200, 2000, 1900]
    }
    df = pd.DataFrame(sample_data)
    
    with st.expander("📊 View Sample Bank Statement Format", expanded=False):
        st.write("Your uploaded bank statement should be in CSV format and look similar to this:")
        st.dataframe(df)
        st.write("Ensure your CSV file has similar columns and formatting for accurate analysis.")

def display_home_page():
    st.title("💰 Personalized Budgeting Assistant")
    st.write("""
    ## Welcome to Your Personalized Budgeting Assistant

    This tool is designed to help you manage your finances effectively. You can analyze your monthly expenses, get insights on your spending habits, and receive tailored financial and budget analysis to achieve your goals.

    ### Key Features:
    - **Expense Tracking**: Visualize where your money is going with intuitive charts.
    - **Financial Insights**: Get personalized advice based on your financial data and proposed budget.
    - **Goal Setting**: Set and track financial goals over time.

    Use the navigation menu to explore the features.
    """)

def display_analysis_page(inputs: UserDataInput):
    st.header("Financial Analysis")
    
    with st.expander("📊 View Sample Bank Statement Format", expanded=True):
        st.write("Your uploaded bank statement should be in CSV format and look similar to this:")
        st.dataframe(display_sample_bank_statement())
        st.write("Ensure your CSV file has similar columns and formatting for accurate analysis.")
    
    try:
        if inputs.bank_statement:
            bank_statement = pd.DataFrame([entry.dict() for entry in inputs.bank_statement])
            
            # Calculate total expenses and deposits
            total_expenses = bank_statement['Withdrawals'].sum()
            total_deposits = bank_statement['Deposits'].sum()
            total_income = inputs.current_income

            # Create categorized expenses dictionary
            categorized_expenses = bank_statement.groupby('Category')['Withdrawals'].sum().dropna().to_dict()

            # Generate charts
            generate_expense_chart(categorized_expenses)
            generate_income_vs_expenses_chart(total_income, total_expenses)

            monthly_savings = total_income - total_expenses
            generate_savings_projection(inputs.current_savings, monthly_savings, inputs.timeline_months)

            # Display financial goals
            if inputs.goals:
                st.subheader("Financial Goals")
                for goal in inputs.goals:
                    st.write(f"• {goal}")

            # Display financial summary
            st.write(escape_dollar_signs(f"Total Income: ${total_income:.2f}"))
            st.write(escape_dollar_signs(f"Total Expenses: ${total_expenses:.2f}"))
            st.write(escape_dollar_signs(f"Monthly Savings: ${monthly_savings:.2f}"))

        else:
            st.warning("No valid bank statement data available. Please upload your bank statement.")
   
    except Exception as e:
        st.error(f"Error displaying analysis: {str(e)}")

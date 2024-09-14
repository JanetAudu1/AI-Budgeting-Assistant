from charts import generate_expense_chart, generate_income_vs_expenses_chart
from advice import generate_advice_ui
import streamlit as st
import pandas as pd

def display_home_page():
    st.title("💰 Personalized Budgeting Assistant")
    st.write("""
    ## Welcome to Your Personalized Budgeting Assistant

    This tool is designed to help you manage your finances effectively. You can analyze your monthly expenses, get insights on your spending habits, and receive tailored financial advice to achieve your goals.

    ### Key Features:
    - **Expense Tracking**: Visualize where your money is going with intuitive charts.
    - **Financial Insights**: Get personalized advice based on your financial data.
    - **Goal Setting**: Set and track financial goals over time.

    Use the navigation menu to explore the features.
    """)

def display_analysis_page(inputs):
    try:
        # Assuming inputs.bank_statement is a pandas DataFrame
        bank_statement = inputs.bank_statement

        if not isinstance(bank_statement, pd.DataFrame):
            st.error("Bank statement data is not in the expected format.")
            return

        # Clean 'Withdrawals' and 'Deposits' columns
        bank_statement['Withdrawals'] = bank_statement['Withdrawals'].replace('[\$,]', '', regex=True).astype(float)
        bank_statement['Deposits'] = bank_statement['Deposits'].replace('[\$,]', '', regex=True).astype(float)

        # Calculate total expenses (sum of all values in the Withdrawals column)
        total_expenses = bank_statement['Withdrawals'].fillna(0).sum()

        # Calculate total deposits (sum of all values in the Deposits column)
        total_deposits = bank_statement['Deposits'].fillna(0).sum()

        # Get total income from user input
        total_income = inputs.current_income

        # Categorize expenses
        categorized_expenses = bank_statement.groupby('Category')['Withdrawals'].sum().to_dict()

        if categorized_expenses and total_income is not None:
            # Generate and display charts
            generate_expense_chart(categorized_expenses)
            generate_income_vs_expenses_chart(total_income, total_expenses)

            # Display additional information
            st.write(f"Total Expenses: ${total_expenses:.2f}")
            st.write(f"Total Deposits: ${total_deposits:.2f}")
            st.write(f"Net Cash Flow: ${total_deposits - total_expenses:.2f}")
        else:
            st.warning("Some financial data is missing. Please make sure to fill out all fields.")
    
    except Exception as e:
        st.error(f"Error displaying analysis: {str(e)}")
        st.exception(e)

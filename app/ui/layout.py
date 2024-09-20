from app.ui.charts import generate_expense_chart, generate_income_vs_expenses_chart
import streamlit as st
import pandas as pd

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

def display_analysis_page(inputs):
    st.header("Financial Analysis")
    
    try:
        if hasattr(inputs, 'bank_statement') and isinstance(inputs.bank_statement, pd.DataFrame):
            bank_statement = inputs.bank_statement
            bank_statement['Withdrawals'] = pd.to_numeric(bank_statement['Withdrawals'], errors='coerce')
            bank_statement['Deposits'] = pd.to_numeric(bank_statement['Deposits'], errors='coerce')

            total_expenses = bank_statement['Withdrawals'].sum()
            total_deposits = bank_statement['Deposits'].sum()
            total_income = inputs.current_income if hasattr(inputs, 'current_income') else total_deposits

            if 'Category' in bank_statement.columns:
                categorized_expenses = bank_statement.groupby('Category')['Withdrawals'].sum().to_dict()
            else:
                categorized_expenses = {'Uncategorized': total_expenses}

            if categorized_expenses and total_income is not None:
                generate_expense_chart(categorized_expenses)
                generate_income_vs_expenses_chart(total_income, total_expenses)

                st.write(f"Total Income: ${total_income:.2f}")
                st.write(f"Total Expenses: ${total_expenses:.2f}")

        else:
            st.warning("No valid bank statement data available. Please upload your bank statement.")
   
    except Exception as e:
        st.error(f"Error displaying analysis: {str(e)}")

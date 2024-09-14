from charts import generate_expense_chart, generate_income_vs_expenses_chart
from advice import generate_advice_ui
import streamlit as st

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
    st.header("🔍 Financial Analysis")

    # Generate and display charts
    generate_income_vs_expenses_chart(inputs['total_income'], inputs['total_expenses'])
    generate_expense_chart(inputs['categorized_expenses'])

    # Generate and display financial advice
    generate_advice_ui(inputs)

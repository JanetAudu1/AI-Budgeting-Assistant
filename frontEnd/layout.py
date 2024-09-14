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

    # Check if required inputs are present before rendering charts
    try:
        categorized_expenses = inputs.get('categorized_expenses')
        total_income = inputs.get('total_income')
        total_expenses = inputs.get('total_expenses')

        if categorized_expenses and total_income is not None and total_expenses is not None:
            # Generate and display charts
            generate_expense_chart(categorized_expenses)
            generate_income_vs_expenses_chart(total_income, total_expenses)

        else:
            st.warning("Some financial data is missing. Please make sure to fill out all fields.")
    
    except Exception as e:
        st.error(f"Error displaying analysis: {str(e)}")

    # Generate and display financial advice
    try:
        generate_advice_ui(inputs)
    except Exception as e:
        st.error(f"Error generating advice: {str(e)}")

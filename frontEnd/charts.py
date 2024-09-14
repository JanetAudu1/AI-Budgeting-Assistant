import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from recommender import generate_advice
from data_validation import UserData

# Chart generation functions
def generate_expense_chart(categorized_expenses):
    # Debugging step: Display raw data for inspection
    st.write("Categorized Expenses Data:", categorized_expenses)

    # Check if there are any expenses to display
    if not categorized_expenses or all(value == 0 for value in categorized_expenses.values()):
        st.markdown("No expense data available.")
        return

    # Convert expenses data into labels and values for charting
    expense_labels = list(categorized_expenses.keys())
    expense_values = list(categorized_expenses.values())

    # Check for non-numerical or None values and remove them
    cleaned_labels = []
    cleaned_values = []
    for label, value in zip(expense_labels, expense_values):
        if isinstance(value, (int, float)) and value > 0:  # Only keep positive numbers
            cleaned_labels.append(label)
            cleaned_values.append(value)

    # Ensure we have data to display after cleaning
    if not cleaned_values:
        st.markdown("No valid expense data available.")
        return

    # Generate the horizontal bar chart
    fig, ax = plt.subplots()
    ax.barh(cleaned_labels, cleaned_values, color='#2C6E49')
    ax.set_xlabel('Amount (USD)')
    ax.set_title('Expenses by Category')
    st.pyplot(fig)

def generate_income_vs_expenses_chart(total_income, total_expenses):
    # Check if income or expenses are valid
    if total_income is None or total_expenses is None:
        st.error("Income or expenses data is missing.")
        return

    st.markdown("### 💰 Income vs. Expenses")
    bar_data = pd.DataFrame({
        'Category': ['Income', 'Expenses'],
        'Amount': [total_income, total_expenses]
    })
    st.bar_chart(bar_data.set_index('Category'))

# Welcome message and navigation setup
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a feature", ["Home", "Budgeting", "Financial Advice"])

# Home page (optional welcome message)
if page == "Home":
    st.title("💰 Personalized Budgeting Assistant")
    st.markdown("""
    ## Welcome to Your Personalized Budgeting Assistant
    
    This tool is designed to help you manage your finances effectively. You can analyze your monthly expenses, get insights on your spending habits, and receive tailored financial advice to achieve your goals.
    
    ### Key Features:
    - **Expense Tracking**: Visualize where your money is going with intuitive charts.
    - **Financial Insights**: Get personalized advice based on your financial data.
    - **Goal Setting**: Set and track financial goals over time.
    
    Use the navigation menu to explore the features.
    """)

# Budgeting feature
elif page == "Budgeting":
    st.title("Personalized Financial Advice and Budgeting")

    # Collect user inputs
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    address = st.text_input("Address")
    current_income = st.number_input("Current Monthly Income", min_value=0.0, format="%.2f")
    current_savings = st.number_input("Current Savings", min_value=0.0, format="%.2f")
    goals = st.text_area("Financial Goals (comma-separated)").split(',')
    timeline_months = st.number_input("Timeline to achieve goals (in months)", min_value=1, step=1)
    bank_statement = st.text_area("Bank Statement (Format: Date | Description | Amount)")
    priorities = st.text_area("Priorities (comma-separated)").split(',')
    savings_goal = st.number_input("Savings Goal", min_value=0.0, format="%.2f")

    # When user clicks the "Generate Advice" button
    if st.button("Generate Financial Advice"):
        try:
            # Create UserData instance from user inputs
            user_data = UserData(
                name=name,
                age=age,
                address=address,
                current_income=current_income,
                current_savings=current_savings,
                goals=goals,
                timeline_months=timeline_months,
                bank_statement=bank_statement,
                priorities=priorities,
                savings_goal=savings_goal
            )

            # Generate financial advice
            advice, financial_data = generate_advice(user_data)

            # Display financial advice
            st.markdown("## 📋 Financial Advice")
            st.write(advice)

            # Generate and display charts
            generate_income_vs_expenses_chart(financial_data['total_income'], financial_data['total_expenses'])
            generate_expense_chart(financial_data['categorized_expenses'])

        except Exception as e:
            st.error(f"Error generating financial advice: {str(e)}")

# Financial advice page (can display advice or historical data if needed)
elif page == "Financial Advice":
    st.title("Your Personalized Financial Advice")
    st.markdown("""
    Here, you will find tailored advice based on your financial data. Make sure you provide your inputs under the 'Budgeting' section.
    """)

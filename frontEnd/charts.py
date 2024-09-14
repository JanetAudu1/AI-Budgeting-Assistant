import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from recommender import generate_advice
from data_validation import UserData

def generate_expense_chart(categorized_expenses):
    st.markdown("### 📊 Breakdown of Monthly Expenses")
    expense_labels = list(categorized_expenses.keys())
    expense_values = list(categorized_expenses.values())

    if expense_values:
        fig, ax = plt.subplots()
        ax.barh(expense_labels, expense_values, color='#2C6E49')
        ax.set_xlabel('Amount (USD)')
        ax.set_title('Expenses by Category')
        st.pyplot(fig)

def generate_income_vs_expenses_chart(total_income, total_expenses):
    st.markdown("### 💰 Income vs. Expenses")
    bar_data = pd.DataFrame({
        'Category': ['Income', 'Expenses'],
        'Amount': [total_income, total_expenses]
    })
    st.bar_chart(bar_data.set_index('Category'))

# Streamlit app
st.title('Personalized Financial Advice and Budgeting')

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

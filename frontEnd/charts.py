import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from recommender import generate_advice

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

# Example inputs for user data (replace this with your own input form)
user_data = {
    'name': 'John Doe',
    'age': 30,
    'address': '123 Main St, New York, NY',
    'current_income': 5000,
    'current_savings': 10000,
    'goals': ['Buy a house', 'Save for retirement'],
    'timeline_months': 12,
    'bank_statement': 'Date | Rent | -2000\nDate | Groceries | -500\nDate | Utilities | -150',
    'priorities': ['Savings', 'Investments'],
    'savings_goal': 15000
}

# Generate financial advice
advice, financial_data = generate_advice(user_data)

# Display financial advice
st.markdown("## 📋 Financial Advice")
st.write(advice)

# Generate and display charts
generate_income_vs_expenses_chart(financial_data['total_income'], financial_data['total_expenses'])
generate_expense_chart(financial_data['categorized_expenses'])

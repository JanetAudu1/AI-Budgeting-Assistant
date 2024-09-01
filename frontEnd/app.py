import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../backEnd')  # Add the backEnd directory to the system path
from recommender import parse_bank_statement, get_financial_advice
from data_validation import UserData  # Ensure this import is present to create a UserData object


# Title of the app
st.title("Personalized Budgeting Assistant")

# User input fields
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
address = st.text_input("Address")
current_income = st.number_input("Current Income ($)", min_value=0.0, format="%.2f")
current_savings = st.number_input("Current Savings ($)", min_value=0.0, format="%.2f")
goals = st.text_area("Goals (separate with commas)", "Buy a house, Save for retirement")
timeline_months = st.number_input("Timeline to achieve goals (months)", min_value=1, step=1)
priorities = st.text_area("Priorities (separate with commas)", "Savings, Investments, Debt Repayment")
bank_statement = st.text_area("Bank Statement", "Paste your bank statement here...")

# Convert goals and priorities to lists
goals_list = [goal.strip() for goal in goals.split(',')]
priorities_list = [priority.strip() for priority in priorities.split(',')]

# Create a UserData object from the input
user_data = UserData(
    name=name,
    age=age,
    address=address,
    current_income=current_income,
    current_savings=current_savings,
    goals=goals_list,
    timeline_months=timeline_months,
    bank_statement=bank_statement,
    priorities=priorities_list
)

# Button to trigger analysis and advice generation
if st.button("Get Budgeting Advice"):
    try:
        # Parse the bank statement
        bank_data = parse_bank_statement(bank_statement)

        # Create a bar chart of major expenses
        st.markdown("### Breakdown of Monthly Expenses")
        expense_labels = [desc for desc, amount in bank_data['major_expenses']]
        expense_values = [amount for desc, amount in bank_data['major_expenses']]

        if expense_values:
            fig, ax = plt.subplots()
            ax.barh(expense_labels, expense_values, color='skyblue')
            ax.set_xlabel('Amount (USD)')
            ax.set_title('Expenses by Category')
            st.pyplot(fig)

        # Bar chart for income vs. expenses
        st.markdown("### Income vs. Expenses")
        bar_data = pd.DataFrame({
            'Category': ['Income', 'Expenses'],
            'Amount': [bank_data['total_income'], bank_data['total_expenses']]
        })
        st.bar_chart(bar_data.set_index('Category'))

        # Generate financial advice
        advice = get_financial_advice(user_data, sources="Investopedia, NerdWallet, Financial Times, Bloomberg, The Wall Street Journal")

        # Display the advice
        st.markdown(f"### Your Financial Advice:\n\n{advice}")

        # Position the sources at the bottom right corner
        st.markdown(
            f"<div style='text-align: right; color: grey; font-size: 0.8em;'>Sources: Investopedia, NerdWallet, Financial Times, Bloomberg, The Wall Street Journal</div>", 
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Failed to generate the budgeting advice: {str(e)}")

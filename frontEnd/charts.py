import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

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


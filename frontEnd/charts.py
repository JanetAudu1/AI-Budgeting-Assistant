import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict

# Chart generation functions
def generate_expense_chart(categorized_expenses: Dict[str, float]):
    if not categorized_expenses or all(value == 0 for value in categorized_expenses.values()):
        st.markdown("No expense data available.")
        return

    expense_labels = list(categorized_expenses.keys())
    expense_values = list(categorized_expenses.values())

    cleaned_labels = []
    cleaned_values = []
    for label, value in zip(expense_labels, expense_values):
        if isinstance(value, (int, float)) and value > 0:
            cleaned_labels.append(label)
            cleaned_values.append(value)

    if not cleaned_values:
        st.markdown("No valid expense data available.")
        return

    fig, ax = plt.subplots()
    ax.barh(cleaned_labels, cleaned_values, color='#2C6E49')
    ax.set_xlabel('Amount (USD)')
    ax.set_title('Expenses by Category')
    st.pyplot(fig)

def generate_income_vs_expenses_chart(total_income: float, total_expenses: float):
    if total_income is None or total_expenses is None:
        st.error("Income or expenses data is missing.")
        return

    st.markdown("### 💰 Income vs. Expenses")
    bar_data = pd.DataFrame({
        'Category': ['Income', 'Expenses'],
        'Amount': [total_income, total_expenses]
    })
    st.bar_chart(bar_data.set_index('Category'))

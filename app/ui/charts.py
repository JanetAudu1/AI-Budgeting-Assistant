import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Chart generation functions
def generate_expense_chart(categorized_expenses):
    if not categorized_expenses:
        st.markdown("No expense data available.")
        return

    df = pd.DataFrame(list(categorized_expenses.items()), columns=['Category', 'Amount'])
    df = df.sort_values('Amount', ascending=False)
    df['Percentage'] = df['Amount'] / df['Amount'].sum() * 100

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(df['Category'], df['Amount'], color='#2C6E49')

    for i, (value, percentage) in enumerate(zip(df['Amount'], df['Percentage'])):
        ax.text(value, i, f'${value:,.2f} ({percentage:.1f}%)', 
                va='center', ha='left', fontweight='bold', fontsize=8, color='white',
                bbox=dict(facecolor='#2C6E49', edgecolor='none', alpha=0.7, pad=2))

    ax.set_xlabel('Amount (USD)')
    ax.set_title('Expenses by Category')
    plt.tight_layout()
    st.pyplot(fig)

def generate_income_vs_expenses_chart(total_income, total_expenses):
    st.markdown("### 💰 Income vs. Expenses")
    bar_data = pd.DataFrame({
        'Category': ['Income', 'Expenses'],
        'Amount': [total_income, total_expenses]
    })
    st.bar_chart(bar_data.set_index('Category'))

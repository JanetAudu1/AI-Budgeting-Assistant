import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sys
from pathlib import Path

# Add the backEnd directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'backEnd'))

from recommender import parse_bank_statement, get_financial_advice
from data_validation import UserData

# Custom CSS for a more sophisticated look
st.markdown("""
    <style>
    .main {background-color: #F5F5F5; font-family: 'Helvetica', sans-serif;}
    h1, h2, h3, h4, h5, h6 {color: #2C6E49;}  /* Muted green */
    .stButton>button {background-color: #2C6E49; color: white; border-radius: 10px; font-size: 16px;}
    .stTextInput>div>input {border-color: #2C6E49;}
    .stNumberInput>div>input {border-color: #2C6E49;}
    .stTextArea>label {font-size: 16px; font-weight: bold; color: #333333;}
    .stTextInput>label {font-size: 16px; font-weight: bold; color: #333333;}
    .stNumberInput>label {font-size: 16px; font-weight: bold; color: #333333;}
    footer {visibility: hidden;}
    .reportview-container .main .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    </style>
    """, unsafe_allow_html=True)

# Title of the app
st.title("💰 Personalized Budgeting Assistant")

# Sidebar for navigation (optional, can be removed if not needed)
st.sidebar.title("📊 Navigation")
options = st.sidebar.radio("Select a Section:", ["Home", "Financial Analysis"])

if options == "Home":
    st.write("""
    ## Welcome to Your Personalized Budgeting Assistant

    This tool is designed to help you manage your finances effectively. You can analyze your monthly expenses, get insights on your spending habits, and receive tailored financial advice to achieve your goals.

    ### Key Features:
    - **Expense Tracking**: Visualize where your money is going with intuitive charts.
    - **Financial Insights**: Get personalized advice based on your financial data.
    - **Goal Setting**: Set and track financial goals over time.

    Use the navigation menu to explore the features.
    """)

elif options == "Financial Analysis":
    st.header("🔍 Financial Analysis")

    # User input fields
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        address = st.text_input("Address")

    with col2:
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
            st.markdown("### 📊 Breakdown of Monthly Expenses")
            expense_labels = [desc for desc, amount in bank_data['major_expenses']]
            expense_values = [amount for desc, amount in bank_data['major_expenses']]

            if expense_values:
                fig, ax = plt.subplots()
                ax.barh(expense_labels, expense_values, color='#2C6E49')  # Muted green for bar chart
                ax.set_xlabel('Amount (USD)')
                ax.set_title('Expenses by Category')
                st.pyplot(fig)

            # Bar chart for income vs. expenses
            st.markdown("### 💰 Income vs. Expenses")
            bar_data = pd.DataFrame({
                'Category': ['Income', 'Expenses'],
                'Amount': [bank_data['total_income'], bank_data['total_expenses']]
            })
            st.bar_chart(bar_data.set_index('Category'))

            # Generate financial advice
            advice = get_financial_advice(user_data, sources="Investopedia, NerdWallet, Financial Times, Bloomberg, The Wall Street Journal")

            # Replace newline characters with HTML line breaks before inserting into the f-string
            formatted_advice = advice.replace('\n', '<br>')

            # Display the advice with a background and padding
            st.markdown(f"<div style='background-color: #E8F5E9; padding: 15px; border-radius: 5px;'>{formatted_advice}</div>", unsafe_allow_html=True)

            # Position the sources at the bottom right corner
            st.markdown(
                f"<div style='text-align: right; color: grey; font-size: 0.8em;'>Sources: Investopedia, NerdWallet, Financial Times, Bloomberg, The Wall Street Journal</div>", 
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Failed to generate the budgeting advice: {str(e)}")


import streamlit as st
import sys
from pathlib import Path
import matplotlib.pyplot as plt

# Add the backEnd directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'backEnd'))

from recommender import generate_advice, plot_income_vs_expenses, plot_categorized_expenses, plot_savings_goal_progress
from data_validation import UserData

def generate_advice_ui(inputs):
    # Ensure 'savings_goal' is included in the inputs dictionary
    savings_goal = inputs.get('savings_goal', 0.0)  # Default to 0.0 if not provided

    # Create the UserData object
    user_data = UserData(
        name=inputs['name'],
        age=inputs['age'],
        address=inputs['address'],
        current_income=inputs['current_income'],
        current_savings=inputs['current_savings'],
        goals=[goal.strip() for goal in inputs['goals'].split(',')],
        timeline_months=inputs['timeline_months'],
        bank_statement=inputs['bank_statement'],
        priorities=[priority.strip() for priority in inputs['priorities'].split(',')],
        savings_goal=savings_goal 
    )
    
    # Generate financial advice using the GPT-enhanced recommender system
    advice, financial_data = generate_advice(user_data)

    # Display the advice with a background and padding
    st.markdown(f"<div style='background-color: #E8F5E9; padding: 15px; border-radius: 5px;'>{advice.replace('\n', '<br>')}</div>", unsafe_allow_html=True)

    # Display Charts
    st.subheader("Financial Overview")

    # Income vs. Expenses Pie Chart
    st.pyplot(plot_income_vs_expenses(financial_data['total_income'], financial_data['total_expenses']))

    # Categorized Expenses Bar Chart
    st.pyplot(plot_categorized_expenses(financial_data['categorized_expenses']))

    # Savings Goal Progress Chart
    st.pyplot(plot_savings_goal_progress(financial_data['total_income'], financial_data['total_expenses'], financial_data['savings_goal']))

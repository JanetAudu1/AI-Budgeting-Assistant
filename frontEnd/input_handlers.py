import streamlit as st 
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / 'backEnd'))

from recommender import parse_bank_statement


def handle_inputs():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=st.session_state.get('name', ''))
        st.session_state['name'] = name

        age = st.number_input("Age", min_value=0, max_value=120, step=1, value=st.session_state.get('age', 0))
        st.session_state['age'] = age

        address = st.text_input("Address", value=st.session_state.get('address', ''))
        st.session_state['address'] = address

    with col2:
        current_income = st.number_input("Current Monthly Income ($)", min_value=0.0, format="%.2f", value=st.session_state.get('current_income', 0.0))
        st.session_state['current_income'] = current_income

        current_savings = st.number_input("Current Savings ($)", min_value=0.0, format="%.2f", value=st.session_state.get('current_savings', 0.0))
        st.session_state['current_savings'] = current_savings

    goals = st.text_area("Goals (separate with commas)", value=st.session_state.get('goals', 'Buy a house, Save for retirement'))
    st.session_state['goals'] = goals

    timeline_months = st.number_input("Timeline to achieve goals (months)", min_value=1, step=1, value=st.session_state.get('timeline_months', 1))
    st.session_state['timeline_months'] = timeline_months

    priorities = st.text_area("Priorities (separate with commas)", value=st.session_state.get('priorities', 'Savings, Investments, Debt Repayment'))
    st.session_state['priorities'] = priorities

    bank_statement = st.text_area("Bank Statement", value=st.session_state.get('bank_statement', 'Paste your bank statement here...'))
    st.session_state['bank_statement'] = bank_statement

    savings_goal = st.number_input("Savings Goal Amount ($)", min_value=0.0, format="%.2f", value=st.session_state.get('savings_goal', 0.0))
    st.session_state['savings_goal'] = savings_goal

    current_debt = st.number_input("Current Debt ($)", min_value=0.0, format="%.2f", value=st.session_state.get('current_debt', 0.0))
    st.session_state['current_debt'] = current_debt

    debt_repayment_goal = st.number_input("Debt Repayment Goal ($)", min_value=0.0, format="%.2f", value=st.session_state.get('debt_repayment_goal', 0.0))
    st.session_state['debt_repayment_goal'] = debt_repayment_goal

    if st.button("Get Budgeting Advice"):
        # Parse the bank statement to get categorized expenses
        categorized_expenses = parse_bank_statement(bank_statement)
        
        # Calculate total expenses
        total_expenses = sum(categorized_expenses.values())

        # total_income is directly from the user input as current_income
        total_income = current_income

        inputs = {
            "name": name,
            "age": age,
            "address": address,
            "current_income": current_income,
            "current_savings": current_savings,
            "goals": goals,
            "timeline_months": timeline_months,
            "priorities": priorities,
            "bank_statement": bank_statement,
            "savings_goal": savings_goal,
            "current_debt": current_debt,
            "debt_repayment_goal": debt_repayment_goal,
            "total_income": total_income,  # Use current_income as total_income
            "total_expenses": total_expenses,  # Total expenses from categorized_expenses
            "categorized_expenses": categorized_expenses,  # Add this line
        }

        return inputs

    return None

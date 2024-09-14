import streamlit as st
from recommender import generate_advice_stream  # or generate_advice depending on your setup
from data_validation import UserData

def generate_advice_ui(inputs):
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
        savings_goal=inputs['savings_goal']
    )
    
    # Generate financial advice (unpack based on how many values the function returns)
    advice, financial_data, _ = generate_advice_stream(user_data)  # Adjusted to unpack three values

    # Display financial advice
    st.markdown("## 📋 Financial Advice")
    st.write(advice)

    # Return financial data for further analysis or charting
    return financial_data


import streamlit as st
from recommender import generate_advice_stream
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
    
    # Generate financial advice
    advice, financial_data = generate_advice_stream(user_data)

    # Replace newline characters with HTML line breaks before inserting into the f-string
    formatted_advice = advice.replace('\n', '<br>')

    # Display the advice with a background and padding
    st.markdown(f"<div style='background-color: #E8F5E9; padding: 15px; border-radius: 5px;'>{formatted_advice}</div>", unsafe_allow_html=True)

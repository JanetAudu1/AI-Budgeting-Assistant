from recommender import generate_advice_stream
from data_validation import UserData
import streamlit as st

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

    # Create a placeholder to stream advice
    advice_placeholder = st.empty()

    # Initialize an empty string to store the complete advice
    complete_advice = ""

    # Stream the advice from the GPT-4 API
    for chunk in generate_advice_stream(user_data):
        # Accumulate advice chunks
        complete_advice += chunk
        # Update the advice_placeholder with the streamed content
        advice_placeholder.text(complete_advice)

    # Return complete advice or financial data as needed (if applicable)
    # If you still need to return the financial data separately:
    return complete_advice

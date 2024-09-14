from recommender import generate_advice_stream  # Import your streaming function
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

    # Create a progress bar and a placeholder for streaming advice
    progress_bar = st.progress(0)
    advice_placeholder = st.empty()
    complete_advice = ""

    # Stream the advice
    for i, chunk in enumerate(generate_advice_stream(user_data)):
        complete_advice += chunk
        advice_placeholder.text(complete_advice)  # Update the advice on the page

        # Update the progress bar (assuming 10 chunks for demonstration)
        progress_bar.progress(min((i + 1) * 10, 100))  # Ensure progress maxes out at 100%

    # Once streaming is complete, remove the progress bar and show a completion message
    progress_bar.empty()
    st.markdown("### ✅ Advice generation complete!")

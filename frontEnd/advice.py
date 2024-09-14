import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backEnd.recommender import generate_advice_stream
from backEnd.data_validation import UserData
import streamlit as st

# Add custom CSS for text wrapping
st.markdown("""
    <style>
    .streamed-advice {
        word-wrap: break-word;
        white-space: normal;
        font-size: 16px;
        max-width: 800px;  /* Set a max width for better readability */
    }
    </style>
    """, unsafe_allow_html=True)

def generate_advice_ui(inputs: UserData):
    # Create the UserData object
    user_data = UserData(
        name=inputs.name,
        age=inputs.age,
        address=inputs.address,
        current_income=inputs.current_income,
        current_savings=inputs.current_savings,
        goals=[goal.strip() for goal in inputs.goals.split(',')],
        timeline_months=inputs.timeline_months,
        bank_statement=inputs.bank_statement,
        priorities=[priority.strip() for priority in inputs.priorities.split(',')],
        savings_goal=inputs.savings_goal
    )

    # Placeholder for streaming output
    advice_placeholder = st.empty()
    complete_advice = ""

    # Initial placeholder message (that will be replaced by streamed content)
    advice_placeholder.text("Generating Financial Advice...")

    # # Generate advice based on user data
    # advice = generate_financial_advice(
    #     name=inputs.name,
    #     age=inputs.age,
    #     address=inputs.address,
    #     current_income=inputs.current_income,
    #     current_savings=inputs.current_savings,
    #     goals=inputs.goals,
    #     timeline_months=inputs.timeline_months,
    #     bank_statement=inputs.bank_statement,
    #     priorities=inputs.priorities,
    #     savings_goal=inputs.savings_goal
    # )

    # Note: You might want to use this 'advice' variable somewhere if you keep this code

    # Stream the GPT response and update the UI dynamically
    for advice_chunk in generate_advice_stream(user_data):
        complete_advice += advice_chunk
        advice_placeholder.markdown(f"<div class='streamed-advice'>{complete_advice}</div>", unsafe_allow_html=True)

    # Once streaming completes, replace with final advice
    st.markdown("### ✅ Advice generation complete!")

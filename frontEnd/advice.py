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
        goals=inputs.goals,  # Assuming goals is already a list
        timeline_months=inputs.timeline_months,
        bank_statement=inputs.bank_statement,  # This is a DataFrame, no need to process it
        priorities=inputs.priorities,  # Assuming priorities is already a list
        savings_goal=inputs.savings_goal
    )

    # Placeholder for streaming output
    advice_placeholder = st.empty()
    complete_advice = ""

    # Initial placeholder message (that will be replaced by streamed content)
    advice_placeholder.text("Generating Financial Advice...")

    try:
        # Stream the GPT response and update the UI dynamically
        for advice_chunk in generate_advice_stream(user_data):
            complete_advice += advice_chunk
            advice_placeholder.markdown(f"<div class='streamed-advice'>{complete_advice}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating advice: {str(e)}")
        st.exception(e)

    if not complete_advice:
        st.warning("No advice was generated. Please check your inputs and try again.")

from recommender import generate_advice_stream  # Import your streaming function
from data_validation import UserData
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

    # Placeholder for streaming output
    advice_placeholder = st.empty()

    # Initial placeholder message (that will be replaced by streamed content)
    advice_placeholder.text("Generating Financial Advice...")

    # Stream the GPT response and update the UI dynamically
    for advice_chunk in generate_advice_stream(user_data):
        # Instead of appending all chunks, just display the new chunk
        advice_placeholder.markdown(f"<div class='streamed-advice'>{advice_chunk}</div>", unsafe_allow_html=True)

    # Once streaming completes, replace with final advice
    st.markdown("### ✅ Advice generation complete!")

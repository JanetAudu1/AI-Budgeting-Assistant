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

    # Create a progress bar and a placeholder for streaming advice
    progress_bar = st.progress(0)
    advice_placeholder = st.empty()

    # Initial message shown while advice is being generated
    advice_placeholder.text("Generating Financial Advice...")

    complete_advice = ""

    # Stream the advice
    for i, chunk in enumerate(generate_advice_stream(user_data)):
        complete_advice += chunk
        # Update the advice in the placeholder with wrapped text (replacing the "Generating Financial Advice..." message)
        advice_placeholder.markdown(f"<div class='streamed-advice'>{complete_advice}</div>", unsafe_allow_html=True)

        # Update the progress bar (assuming 10 chunks for demonstration)
        progress_bar.progress(min((i + 1) * 10, 100))  # Ensure progress maxes out at 100%

    # Once streaming is complete, remove the progress bar
    progress_bar.empty()

    # Ensure only the final complete advice is shown (replace the "Generating Financial Advice..." message)
    advice_placeholder.markdown(f"<div class='streamed-advice'>{complete_advice}</div>", unsafe_allow_html=True)

    # Show a completion message
    st.markdown("### ✅ Advice generation complete!")


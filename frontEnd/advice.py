import streamlit as st
import sys
from pathlib import Path

# Add the backEnd directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'backEnd'))

from recommender import generate_advice
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
        priorities=[priority.strip() for priority in inputs['priorities'].split(',')]
    )
    
    # Generate financial advice
    advice = generate_advice(user_data, sources="Investopedia, NerdWallet, Financial Times, Bloomberg, The Wall Street Journal")

    # Replace newline characters with HTML line breaks before inserting into the f-string
    formatted_advice = advice.replace('\n', '<br>')

    # Display the advice with a background and padding
    st.markdown(f"<div style='background-color: #E8F5E9; padding: 15px; border-radius: 5px;'>{formatted_advice}</div>", unsafe_allow_html=True)

    # Position the sources at the bottom right corner
    st.markdown(
        f"<div style='text-align: right; color: grey; font-size: 0.8em;'>Sources: Investopedia, NerdWallet, Financial Times, Bloomberg, The Wall Street Journal</div>", 
        unsafe_allow_html=True
    )


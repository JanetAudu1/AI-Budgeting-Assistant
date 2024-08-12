import streamlit as st
import requests
import json

# Set up the API URL (ensure this matches where your FastAPI app is running)
API_URL = "http://localhost:8000/get_advice"

# Title of the app
st.title("Financial Advice Recommender")

# User input fields
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
address = st.text_input("Address")
current_income = st.number_input("Current Income ($)", min_value=0.0, format="%.2f")
current_savings = st.number_input("Current Savings ($)", min_value=0.0, format="%.2f")
goals = st.text_area("Goals (separate with commas)", "Buy a house, Save for retirement")
timeline_months = st.number_input("Timeline to achieve goals (months)", min_value=1, step=1)
priorities = st.text_area("Priorities (separate with commas)", "Savings, Investments, Debt Repayment")
bank_statement = st.text_area("Bank Statement", "Paste your bank statement here...")

# Convert goals and priorities to lists
goals_list = [goal.strip() for goal in goals.split(',')]
priorities_list = [priority.strip() for priority in priorities.split(',')]

# Create a dictionary with the user data
user_data = {
    "name": name,
    "age": age,
    "address": address,
    "current_income": current_income,
    "current_savings": current_savings,
    "goals": goals_list,
    "timeline_months": timeline_months,
    "bank_statement": bank_statement,
    "priorities": priorities_list
}

# Button to submit data
if st.button("Get Financial Advice"):
    # Make a request to the FastAPI recommender
    try:
        response = requests.post(API_URL, json=user_data)
        response_data = response.json()
        
        if response.status_code == 200:
            st.success("Advice received successfully!")
            st.markdown("### Your Financial Advice")
            st.markdown(response_data["advice"], unsafe_allow_html=True)
        else:
            st.error(f"Error: {response_data['detail']}")
    
    except Exception as e:
        st.error(f"Failed to connect to the recommender API: {str(e)}")


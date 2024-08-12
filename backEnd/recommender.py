import os
import openai
import pandas as pd
from data_validation import UserData
from fastapi import HTTPException

# Load the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

def parse_bank_statement(bank_statement: str) -> dict:
    """Parse the bank statement and extract financial data."""
    # Dummy implementation: Replace with actual parsing logic
    return {
        "total_income": 5000,
        "total_expenses": 3000,
        "savings_rate": 2000,
        "major_expenses": ["Rent", "Utilities", "Groceries"]
    }

def get_financial_advice(user_data: UserData, sources: str) -> str:
    """Generate financial advice based on user data."""
    try:
        bank_data = parse_bank_statement(user_data.bank_statement)
        
        # Construct a string that represents the user's priorities
        priority_string = ", ".join(user_data.priorities)
        
        messages = [
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": (
                f"Provide personalized financial advice based on the following details:\n\n"
                f"Name: {user_data.name}\n"
                f"Age: {user_data.age}\n"
                f"Address: {user_data.address}\n"
                f"Current Income: ${user_data.current_income}/month\n"
                f"Current Savings: ${user_data.current_savings}\n"
                f"Goals: {', '.join(user_data.goals)}\n"
                f"Timeline to achieve goals: {user_data.timeline_months} months\n"
                f"Bank Data: {bank_data}\n"
                f"User Priorities: {priority_string}\n\n"
                f"Please prioritize the advice based on the user's stated priorities.\n\n"
                f"Use validated financial principles from sources such as {sources}."
            )}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response['choices'][0]['message']['content'].strip()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating financial advice: {str(e)}")

def format_advice_to_table(advice: str, sources: str) -> str:
    """Format financial advice into an HTML table."""
    data = {
        "Advice": [advice],
        "Sources": [sources]
    }
    df = pd.DataFrame(data)
    return df.to_html(index=False)


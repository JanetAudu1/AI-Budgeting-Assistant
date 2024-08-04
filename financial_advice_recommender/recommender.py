import os
import openai
from data_validation import UserData
import pandas as pd

# Load the API key from the environment variable
openai.api_key = "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"

if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

#openai.api_keyopenai.api_key = api_key
#openai.api_key = ""  # Replace with your actual OpenAI API Key
#client = OpenAI()

#client = OpenAI(api_key=openai.api_key)

def parse_bank_statement(bank_statement: str) -> dict:
    # Dummy implementation: In real case, you would use a parser to extract meaningful information
    # Here we simply return dummy parsed data
    return {
        "total_income": 5000,
        "total_expenses": 3000,
        "savings_rate": 2000,
        "major_expenses": ["Rent", "Utilities", "Groceries"]
    }

def get_financial_advice(user_data: UserData) -> str:
    bank_data = parse_bank_statement(user_data.bank_statement)
    
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
            f"Bank Data: {bank_data}\n\n"
            f"Consider valid financial advice and strategies to help the user save money and achieve their goals within the given timeline."
        )}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    return response['choices'][0]['message']['content'].strip()

def format_advice_to_table(advice: str, sources: str) -> str:
    data = {
        "Advice": [advice],
        "Sources": [sources]
    }
    df = pd.DataFrame(data)
    return df.to_html(index=False)


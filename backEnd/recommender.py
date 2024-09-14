import openai
import os
from typing import List, Dict
from backEnd.data_validation import UserData

# Set your OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

def categorize_expenses(description: str) -> str:
    """
    Categorizes the expense based on keywords in the description.
    """
    categories = {
        "rent": ["rent", "rents"],
        "utilities": ["utility", "utilities"],
        "groceries": ["grocery", "groceries"],
    }

    description_lower = description.lower()
    for category, keywords in categories.items():
        if any(keyword in description_lower for keyword in keywords):
            return category
    return "discretionary"  # Default category if no match

def parse_bank_statement(bank_statement: str) -> Dict[str, float]:
    """
    Parses the bank statement and categorizes the expenses.
    Returns a dictionary where keys are categories and values are the total amounts spent.
    """
    lines = bank_statement.strip().splitlines()
    categorized_expenses = {"rent": 0, "utilities": 0, "groceries": 0, "discretionary": 0}

    for line in lines:
        if '|' in line and 'Date' not in line:
            parts = [part.strip() for part in line.split('|')]
            if len(parts) >= 3:
                description = parts[1]
                amount_str = parts[2]

                # Convert the amount string to a float
                if amount_str:
                    try:
                        amount = float(amount_str.replace('+', '').replace('-', '').replace(',', ''))
                        if '-' in amount_str:
                            amount = -amount  # Convert negative expenses
                    except ValueError:
                        continue

                    # Categorize the expense based on the description
                    category = categorize_expenses(description)
                    categorized_expenses[category] += abs(amount)

    return categorized_expenses

def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    """
    Calculates the savings rate based on income and expenses.
    """
    if total_income == 0:
        return 0  # Avoid division by zero
    return (total_income - total_expenses) / total_income * 100

def generate_advice_stream(user_data: UserData):
    """
    Generates personalized financial advice and streams the response from GPT-4.
    """
    try:
        # Use the user-provided income directly
        total_income = user_data.current_income

        # Parse categorized expenses from the bank statement
        categorized_expenses = parse_bank_statement(user_data.bank_statement)

        # Calculate the total expenses and savings rate
        total_expenses = sum(categorized_expenses.values())
        savings_rate = calculate_savings_rate(total_income, total_expenses)

        # Create user context for GPT advice
        user_context = {
            "name": user_data.name,
            "income": total_income,
            "expenses": total_expenses,
            "savings_rate": savings_rate,
            "goals": user_data.goals,
            "timeline": user_data.timeline_months,
            "priorities": user_data.priorities,
            "savings_goal": user_data.savings_goal,
            "age": user_data.age,
            "location": user_data.address
        }

        # Construct GPT prompt for chat completion
        gpt_prompt = (
            "You are a knowledgeable financial advisor AI Chatbot called 'SmartBudget AI' specializing in personalized financial planning. "
            "Your task is to provide financial advice based on the following user details:\n"
            f"Name: {user_context['name']}\n"
            f"Income: ${user_context['income']:.2f}\n"
            f"Expenses: ${user_context['expenses']:.2f}\n"
            f"Savings Rate: {user_context['savings_rate']:.2f}%\n"
            f"Goals: {', '.join(user_context['goals'])}\n"
            f"Timeline to achieve goals: {user_context['timeline']} months\n"
            f"Savings Goal: ${user_context['savings_goal']:.2f}\n"
            "Provide personalized financial advice to help the user achieve their savings goal and optimize expenses."
        )

        # Stream the GPT-4 response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly and helpful financial advisor."},
                {"role": "user", "content": gpt_prompt}
            ],
            stream=True  # Enable streaming
        )

        # Yield the response chunks to the caller
        for chunk in response:
            content = chunk['choices'][0]['delta'].get('content', '')
            if content:
                yield content

    except Exception as e:
        yield f"Error generating advice: {str(e)}"

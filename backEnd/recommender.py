import openai
import os
from typing import List, Dict
from data_validation import UserData

# Option 1: Set your OpenAI API key directly in the code (not recommended for production)
# Uncomment the following line and replace with your API key
# openai.api_key = "your-openai-api-key"

# Option 2: Set your OpenAI API key as an environment variable
# This is more secure and flexible. You can set the environment variable OPENAI_API_KEY in your OS.
openai.api_key = os.getenv("OPENAI_API_KEY")

# If you prefer storing the key in a file, uncomment the following line and provide the file path
# openai.api_key_path = "/path/to/your/api_key.txt"

def categorize_expenses(description: str) -> str:
    categories = {
        "rent": ["rent", "rents"],
        "utilities": ["utility", "utilities"],
        "groceries": ["grocery", "groceries"],
    }
    
    description_lower = description.lower()
    for category, keywords in categories.items():
        if any(keyword in description_lower for keyword in keywords):
            return category
    return "discretionary"  # Default to discretionary if no match

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
                
                # Convert amount_str to a float
                if amount_str:
                    try:
                        amount = float(amount_str.replace('+', '').replace('-', '').replace(',', ''))
                    except ValueError:
                        continue

                    # Categorize the expenses based on the description
                    category = categorize_expenses(description)
                    if amount_str.startswith('-'):  # Only count the expenses
                        categorized_expenses[category] += amount

    return categorized_expenses

def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    if total_income == 0:
        return 0  # Avoid division by zero
    savings_rate = (total_income - total_expenses) / total_income * 100
    return savings_rate

def generate_advice(user_data: UserData) -> (str, Dict[str, float]):
    try:
        # Use the user-provided income directly
        total_income = user_data.current_income

        # Parse categorized expenses from the bank statement
        categorized_expenses = parse_bank_statement(user_data.bank_statement)
        
        # Calculate the total expenses from categorized expenses
        total_expenses = sum(categorized_expenses.values())
        
        # Calculate the savings rate based on user-provided income
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

        # Construct GPT prompt for chat completion (without the sequential steps)
        gpt_prompt = (
            "You are a knowledgeable financial advisor AI Chatbot called 'SmartBudget AI' specializing in personalized financial planning. "
            "Your expertise lies in thoroughly analyzing the user's financial data, including their income, expenses, savings goals, and priorities, to offer personalized, actionable advice on how to achieve financial success. "
            "You are tasked with providing the user with financial advice based on the financial details they have provided in the system content. "
            "Your responses should only focus on financial-related inquiries. Please address the user by name where appropriate. "
            "Here are the details provided by the user:\n"
            f"Name: {user_context['name']}\n"
            f"Income: ${user_context['income']:.2f}\n"
            f"Expenses: ${user_context['expenses']:.2f}\n"
            f"Savings Rate: {user_context['savings_rate']:.2f}%\n"
            f"Goals: {', '.join(user_context['goals'])}\n"
            f"Timeline to achieve goals: {user_context['timeline']} months\n"
            f"Savings Goal: ${user_context['savings_goal']:.2f}\n"
            "It's important to consider the user's age, location, income, expenses, financial goals, and savings priorities while formulating your advice. Ensure your advice is well-reasoned and tailored to the information provided by the user. "
            "For example, if a user has a goal of saving for retirement and is currently saving 10% of their income, you can suggest ways to optimize expenses and increase their savings rate to achieve this goal faster. "
            "Please provide well-reasoned and actionable financial advice based on the details provided."
        )

        # Send the prompt to GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful and friendly financial advisor."},
                {"role": "user", "content": gpt_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        advice = response['choices'][0]['message']['content'].strip()

        # Prepare financial data for returning
        financial_data = {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "categorized_expenses": categorized_expenses,
            "savings_rate": savings_rate,
            "savings_goal": user_data.savings_goal
        }

        return advice, financial_data

    except Exception as e:
        raise Exception(f"Error generating financial advice: {str(e)}")

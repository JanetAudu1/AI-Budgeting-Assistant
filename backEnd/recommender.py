import openai
import matplotlib.pyplot as plt
from io import BytesIO
from typing import List, Dict
import base64
from data_validation import UserData

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

def parse_bank_statement(bank_statement: str) -> (float, float, Dict[str, float]):
    lines = bank_statement.strip().splitlines()
    total_income = 0
    total_expenses = 0
    categorized_expenses = {"rent": 0, "utilities": 0, "groceries": 0, "discretionary": 0}

    for line in lines:
        if '|' in line and 'Date' not in line:
            parts = [part.strip() for part in line.split('|')]
            if len(parts) >= 3:
                description = parts[1]
                amount_str = parts[2]
                
                if amount_str:
                    try:
                        amount = float(amount_str.replace('+', '').replace('-', '').replace(',', ''))
                    except ValueError:
                        continue

                    category = categorize_expenses(description)
                    if amount_str.startswith('-'):
                        categorized_expenses[category] += amount
                        total_expenses += amount
                    else:
                        total_income += amount

    return total_income, total_expenses, categorized_expenses

def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    if total_income == 0:
        return 0  # Avoid division by zero
    savings_rate = (total_income - total_expenses) / total_income * 100
    return savings_rate

def generate_advice(user_data: UserData) -> (str, Dict[str, float]):
    try:
        # Parse bank statement and calculate metrics
        total_income, total_expenses, categorized_expenses = parse_bank_statement(user_data.bank_statement)
        savings_rate = calculate_savings_rate(total_income, total_expenses)

        # User data to provide to GPT for context
        user_context = {
            "name": user_data.name,
            "income": total_income,
            "expenses": total_expenses,
            "savings_rate": savings_rate,
            "goals": user_data.goals,
            "timeline": user_data.timeline_months,
            "priorities": user_data.priorities,
            "savings_goal": user_data.savings_goal
        }

        # Construct GPT prompt for chat completion
        gpt_prompt = f"""
        You are a friendly and knowledgeable financial advisor. Here’s the financial situation of {user_context['name']}:
        - Total Income: ${user_context['income']:.2f}
        - Total Expenses: ${user_context['expenses']:.2f}
        - Savings Rate: {user_context['savings_rate']:.2f}%
        {user_context['name']} has the following financial goals: {', '.join(user_context['goals'])}. 
        The timeline to achieve these goals is {user_context['timeline']} months. 
        Provide personalized and friendly financial advice on how to achieve these goals, including tips on optimizing expenses and reaching the savings goal of ${user_context['savings_goal']:.2f}.
        """

        # Call OpenAI's Chat API for generating advice
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial assistant."},
                {"role": "user", "content": gpt_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        # Extract the generated advice
        advice = response['choices'][0]['message']['content'].strip()

        # Return advice and financial data for charting
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

def plot_income_vs_expenses(income: float, expenses: float):
    labels = ['Saved', 'Spent']
    sizes = [income - expenses, expenses]
    colors = ['#4CAF50', '#FF5722']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig

def plot_categorized_expenses(expenses: Dict[str, float]):
    labels = expenses.keys()
    values = expenses.values()
    
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['#2196F3', '#FFC107', '#FF5722', '#9C27B0'])
    ax.set_ylabel('Amount ($)')
    ax.set_title('Categorized Expenses')

    return fig

def plot_savings_goal_progress(income: float, expenses: float, savings_goal: float):
    saved = income - expenses
    progress = min(saved / savings_goal, 1.0)

    fig, ax = plt.subplots()
    ax.barh(['Savings Goal Progress'], [progress], color='#4CAF50')
    ax.set_xlim([0, 1])
    ax.set_xlabel('Progress (%)')

    return fig

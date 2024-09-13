import openai
from typing import List, Dict
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

def generate_advice(user_data: UserData) -> str:
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

        return advice

    except Exception as e:
        raise Exception(f"Error generating financial advice: {str(e)}")

import openai
import os
from typing import List, Dict
from .data_validation import UserData

# Set your OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    """
    Calculate the savings rate based on total income and expenses.

    Args:
        total_income (float): The total income of the user.
        total_expenses (float): The total expenses of the user.

    Returns:
        float: The calculated savings rate as a percentage.
    """
    if total_income == 0:
        return 0  # Avoid division by zero
    return (total_income - total_expenses) / total_income * 100

def generate_advice_stream(user_data: UserData):
    """
    Generate personalized financial advice and stream the response from GPT-4.

    Args:
        user_data (UserData): The user's financial data and goals.

    Yields:
        str: Chunks of generated financial advice.

    Raises:
        Exception: If there's an error in generating the advice.
    """
    try:
        # Use the user-provided income directly
        total_income = user_data.current_income

        # Parse categorized expenses from the bank statement
        bank_statement = user_data.bank_statement
        categorized_expenses = bank_statement.groupby('Category')['Withdrawals'].sum().to_dict()

        # Calculate the total expenses and savings rate
        total_expenses = bank_statement['Withdrawals'].sum()
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
            "location": user_data.address,
            "categorized_expenses": categorized_expenses
        }

        #  GPT prompt for recommendations
        gpt_prompt = f"""You are a knowledgeable financial advisor AI Chatbot specializing in personalized financial planning. 
        Your task is to provide detailed financial advice based on the following user details:

        Name: {user_context['name']}
        Age: {user_context['age']}
        Location: {user_context['location']}
        Monthly Income: ${user_context['income']:.2f}
        Monthly Expenses: ${user_context['expenses']:.2f}
        Current Savings Rate: {user_context['savings_rate']:.2f}%
        Financial Goals: {', '.join(user_context['goals'])}
        Timeline to achieve goals: {user_context['timeline']} months
        Savings Goal: ${user_context['savings_goal']:.2f}
        Priorities: {', '.join(user_context['priorities'])}

        Categorized Expenses:
        {', '.join([f'{category}: ${amount:.2f}' for category, amount in user_context['categorized_expenses'].items()])}

        Please provide comprehensive, personalized financial advice to help the user achieve their savings goal and optimize expenses. Include specific strategies for budgeting, saving, and investing based on their unique situation and goals.

        Important: When suggesting budget cuts or changes in spending habits, always provide:
        1. A clear explanation of WHY the cut or change is necessary or beneficial.
        2. Specific, actionable advice on HOW to implement the suggested cut or change.
        3. If possible, quantify the potential impact of the suggested change.

        For example, instead of just saying "Reduce dining out expenses", say something like:
        "Consider reducing your dining out expenses by 30% (WHY) This could save you approximately $X per month, which would significantly accelerate your progress towards your savings goal. (HOW) You can achieve this by:
        1. Cooking at home 2 more nights per week and bringing lunch to work 3 days a week.
        2. Using meal planning and grocery lists to make home cooking more efficient and cost-effective.
        3. When dining out, look for happy hour specials or use restaurant discount apps."

        Provide this level of detail and explanation for each significant recommendation in your advice. Further more, ensure that the text outputted is not garbled and it is spaced and formatted properly.
        """

        # Call OpenAI API to generate advice
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": gpt_prompt}
            ],
            #  max_tokens=200,  # Control the token output length
             temperature=0.7,  # Adjust the randomness
             frequency_penalty=0.5, # To control repetition
             stream=True
        )

        # Stream the response
        for chunk in response:
            if chunk['choices'][0]['finish_reason'] is not None:
                break
            yield chunk['choices'][0]['delta'].get('content', '')

    except Exception as e:
        yield f"Error generating advice: {str(e)}"

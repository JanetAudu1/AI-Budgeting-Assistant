import openai
import os
from typing import List, Dict
from .data_validation import UserData
from backEnd.config import get_sources

# Set OpenAI API key from environment variable
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
            "age": user_data.age,
            "location": user_data.address,
            "categorized_expenses": categorized_expenses
           
        }

        # Helper function to format optional numeric fields
        def format_optional_numeric(value):
            return f"${value:.2f}" if value is not None else "Not specified"

        # Get financial sources
        sources = get_sources()
        
        #  GPT prompt for recommendations
        gpt_prompt = f"""
            You are a knowledgeable budgeting assistant specializing in personalized financial planning.
            Your advice is based on information from reputable sources, including: {sources}

            Your task is to provide thorough and professional financial advice based on the following user details:

            Name: {user_context['name']}
            Age: {user_context['age']}
            Location: {user_context['location']}
            Monthly Income: ${user_context['income']:.2f}
            Monthly Expenses: ${user_context['expenses']:.2f}
            Current Savings Rate: {user_context['savings_rate']:.2f}%
            Financial Goals: {', '.join(user_context['goals'])}
            Timeline to achieve goals: {user_context['timeline']} months
            Priorities: {', '.join(user_context['priorities']) if user_context['priorities'] else 'Not specified'}

            Categorized Expenses:
            {', '.join([f'{category}: ${amount:.2f}' for category, amount in user_context['categorized_expenses'].items()])}

            After analyzing the user's details, please offer professional advice that includes:
            1. A breakdown of current financial habits.
            2. Recommendations for improving savings and reaching the user's financial goals within the specified timeline.
            3. Insights on how to better align monthly spending with the user's priorities and goals.

            Once the financial advice is complete, generate a proposed monthly budget based on the recommendations shared, ensuring it is realistic and tailored to the user's goals.

            At the end of your advice, include the following separator:
            ---BUDGET_JSON_START---
            Then, provide the budget as a JSON object like this:
            {{
                "Proposed Monthly Budget": {{
                    "Category1": amount1,
                    "Category2": amount2,
                    ...
                }}
            }}
            Followed by:
            ---BUDGET_JSON_END---

            After the JSON, conclude your advice with: "Best of luck with your financial journey, {user_context['name']}!"
        """
        # Call OpenAI API to generate advice
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": gpt_prompt}
            ],
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

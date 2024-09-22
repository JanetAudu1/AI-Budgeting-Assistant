import openai
import os
from typing import List, Dict
from app.core.data_validation import UserData
from app.core.config import get_sources
from dotenv import load_dotenv
load_dotenv()

def setup_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")
    openai.api_key = api_key

def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    """
    Calculate the savings rate based on total income and expenses.
    """
    if total_income == 0:
        return 0  # Avoid division by zero
    return (total_income - total_expenses) / total_income * 100

def prepare_user_context(user_data: UserData) -> Dict:
    total_income = user_data.current_income
    bank_statement = user_data.bank_statement
    categorized_expenses = bank_statement.groupby('Category')['Withdrawals'].sum().to_dict()
    total_expenses = bank_statement['Withdrawals'].sum()
    savings_rate = calculate_savings_rate(total_income, total_expenses)

    return {
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

def create_gpt_prompt(user_context: Dict, sources: List[str]) -> str:
    return f"""
    You are a friendly, professional budgeting expert. Your advice is based on comprehensive analysis and information from reputable sources including: {sources}

    Your task is to provide detailed, yet approachable financial advice based on the following details:

    Name: {user_context['name']}
    Age: {user_context['age']}
    Location: {user_context['location']}
    Monthly Income: ${user_context['income']:.2f}
    Monthly Expenses: ${user_context['expenses']:.2f}
    Current Savings Rate: {user_context['savings_rate']:.2f}%
    Financial Goals: {', '.join(user_context['goals'])}
    Timeline to achieve goals: {user_context['timeline']} months
    Financial Priorities: {', '.join(user_context['priorities']) if user_context['priorities'] else 'Not specified'}

    Expense Breakdown:
    {', '.join([f'{category}: ${amount:.2f}' for category, amount in user_context['categorized_expenses'].items()])}

    Provide a friendly, comprehensive financial analysis and actionable advice tailored to {user_context['name']}'s situation. Your recommendations should be strategic and data-driven, but explained in an easy-to-understand manner.

    Assess whether {user_context['name']}'s financial goals are achievable within their {user_context['timeline']}-month timeline. Clearly state if each goal is realistically attainable, and if not, suggest friendly adjustments to either the goals or their financial approach.

    After your advice, create a proposed monthly budget that reflects your recommendations and aligns with {user_context['name']}'s financial goals. The budget should:
    1. Total exactly to their monthly income of ${user_context['income']:.2f}.
    2. Not include income as a category.
    3. Be structured to meet their savings goals if possible, considering their {user_context['timeline']}-month timeline and other financial priorities.
    4. Use specific, descriptive category names that align with common budgeting practices and their unique situation.

    At the end of your advice, include this separator:
    ---BUDGET_JSON_START---
    Then, provide the proposed monthly budget as a JSON object:
    {{
        "Proposed Monthly Budget": {{
            "Category1": amount1,
            "Category2": amount2,
            ...
        }}
    }}
    Followed by:
    ---BUDGET_JSON_END---

    After the budget JSON, briefly summarize if this budget allows {user_context['name']} to meet their goals within their {user_context['timeline']}-month timeline. If not, suggest what adjustments might be needed to either the goals or the timeline.

    Conclude your friendly advice with: "I'm excited to support you on your journey to financial success, {user_context['name']}! If you have any questions about this plan, please don't hesitate to ask. You've got this!"
    """

def call_openai_api(prompt: str):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are a helpful budgeting assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        frequency_penalty=0.5,
        stream=True
    )

def generate_advice_stream(user_data: UserData):
    """
    Generate personalized financial advice and stream the response from GPT-4.
    """
    try:
        setup_openai()
        user_context = prepare_user_context(user_data)
        sources = get_sources()
        gpt_prompt = create_gpt_prompt(user_context, sources)
        response = call_openai_api(gpt_prompt)

        for chunk in response:
            if chunk['choices'][0]['finish_reason'] is not None:
                break
            yield chunk['choices'][0]['delta'].get('content', '')

    except Exception as e:
        yield f"Error generating advice: {str(e)}"

import openai
import os
from typing import List, Dict
from app.api.models import UserDataInput
from app.core.config import get_sources
from dotenv import load_dotenv
import torch
import logging
from functools import lru_cache
import time
from .model_handlers import handle_huggingface_model, handle_gpt4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    """
    Calculate the savings rate based on total income and expenses.
    """
    if total_income == 0:
        return 0  # Avoid division by zero
    return (total_income - total_expenses) / total_income * 100

def prepare_user_context(user_data: UserDataInput) -> Dict:
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
        "age": user_data.age,
        "location": user_data.address,
        "categorized_expenses": categorized_expenses
    }

def create_gpt_prompt(user_context: Dict, sources: List[str]) -> str:
    logger.info(f"Creating prompt for {user_context['selected_llm']} model")
    return f"""
    You are a friendly, professional budgeting expert. Your advice is based on comprehensive analysis and information from reputable sources including: {sources}

    Your task is to provide detailed, yet approachable financial advice based on the following details:

    Name: {user_context['name']}
    Age: {user_context['age']}
    Location: {user_context['location']}
    Monthly Income: ${float(user_context['income']):.2f}
    Monthly Expenses: ${float(user_context['expenses']):.2f}
    Current Savings Rate: {float(user_context['savings_rate']):.2f}%
    Financial Goals: {', '.join(user_context['goals'])}

    Expense Breakdown:
    {', '.join([f'{category}: ${float(amount):.2f}' for category, amount in user_context['categorized_expenses'].items()])}

    Provide a friendly, comprehensive financial analysis and actionable advice tailored to {user_context['name']}'s situation. Your recommendations should be strategic and data-driven, but explained in an easy-to-understand manner.

    Assess whether {user_context['name']}'s financial goals are achievable. Clearly state if each goal is realistically attainable, and if not, stress the point that the goals are not realistic and suggest friendly adjustments to either the goals or their financial approach.

    After your advice, create a proposed monthly budget that reflects your recommendations and aligns with {user_context['name']}'s financial goals. The budget should:
    1. Total exactly to their monthly income of ${float(user_context['income']):.2f}.
    2. Not include income as a category.
    3. Be structured to meet their savings goals if possible, considering their financial priorities.
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

    After the budget JSON, briefly summarize if this budget allows {user_context['name']} to meet their goals. If not, stress the point that the goals are not realistic and suggest what adjustments might be needed to either the goals or the timeline.

    Conclude your friendly advice with: "You are already doing great and working towards your goals, {user_context['name']}! You've got this!"
    """

def call_llm_api(prompt: str, model_name: str, timeout: int = 30):
    try:
        if model_name == "GPT-4":
            return handle_gpt4(prompt)
        else:
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    return handle_huggingface_model(prompt, model_name)
                except RuntimeError as e:
                    if "CUDA out of memory" in str(e):
                        torch.cuda.empty_cache()
                        continue
                    else:
                        print(f"RuntimeError occurred: {str(e)}")
                        raise
            raise TimeoutError(f"Model {model_name} timed out after {timeout} seconds")
    except Exception as e:
        error_message = f"Error loading or running {model_name}: {str(e)}"
        print(error_message)
        return error_message

def generate_advice_stream(user_data: UserDataInput):
    try:
        user_context = prepare_user_context(user_data)
        sources = get_sources()
        gpt_prompt = create_gpt_prompt(user_context, sources)
        response = call_llm_api(gpt_prompt, user_data.selected_llm)

        yield response

    except Exception as e:
        yield f"Error generating advice: {str(e)}"
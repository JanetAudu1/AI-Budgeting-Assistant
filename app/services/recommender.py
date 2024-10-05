from typing import List, Dict, Tuple, Optional, Any
from app.api.models import UserDataInput, BankStatementEntry
from app.core.config import get_sources
from dotenv import load_dotenv
import torch
import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from .model_handlers import handle_huggingface_model, handle_gpt4
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    """
    Calculate the savings rate based on total income and expenses.
    """
    if total_income == 0:
        return 0  # Avoid division by zero
    return (total_income - total_expenses) / total_income * 100

def prepare_user_context(user_data: UserDataInput) -> Dict[str, Any]:
    try:
        bank_statement_df = pd.DataFrame([entry.dict() for entry in user_data.bank_statement])
        total_expenses = bank_statement_df['Withdrawals'].sum()
        savings_rate = calculate_savings_rate(user_data.current_income, total_expenses)

        return {
            "name": user_data.name,
            "age": user_data.age,
            "address": user_data.address,
            "income": user_data.current_income,
            "current_savings": user_data.current_savings,
            "goals": user_data.goals,
            "timeline_months": user_data.timeline_months,
            "expenses": total_expenses,
            "savings_rate": savings_rate,
            "selected_llm": user_data.selected_llm
        }
    except Exception as e:
        return {"error": str(e)}

def create_gpt_prompt(user_data: UserDataInput, sources: List[str], follow_up_question: str = None) -> Tuple[str, str]:
    print(f"Creating prompt with income: ${user_data.current_income:.2f}")
    
    system_message = f"""You are a friendly, empathetic professional budget advisor. Provide a detailed yet approachable financial analysis and budgeting advice for the following client. Use a warm, first-person perspective as if you're having a conversation with a friend. The client's monthly income is EXACTLY ${user_data.current_income:.2f}. 
    Always use this exact income figure in your analysis and advice. Do not assume or use any other income figure."""
    
    prompt = f"""
    Based on the following user information and financial data, provide a comprehensive financial analysis and advice:

    Name: {user_data.name}
    Age: {user_data.age}
    State: {user_data.state}  # Changed from 'Location' to 'State'
    Monthly Income: ${user_data.current_income:.2f}
    Current Savings: ${user_data.current_savings:.2f}
    Financial Goals: {', '.join(user_data.goals)}
    Timeline: {user_data.timeline_months} months

    Bank Statement Summary:
    Total Withdrawals: ${sum(entry.Withdrawals for entry in user_data.bank_statement):.2f}

    Budgeting Constraints:
    {format_constraints(user_data.constraints)}

    Top Expense Categories:
    {get_top_expenses(user_data.bank_statement)}

    IMPORTANT: The client's monthly income is EXACTLY ${user_data.current_income:.2f}. Do not use any other income figure in your analysis or advice. This is the correct and only income figure to use.
    Please provide the following:
    1. Income and Expense Analysis
    2. Savings Rate Evaluation
    3. Goal Feasibility
    4. Recommendations for Improvement
    5. Proposed Monthly Budget (in JSON format)

    Use the following format for the Proposed Monthly Budget:
    ---BUDGET_JSON_START---
    {{
      "Proposed Monthly Budget": {{
        "Category1": {{"proposed_change": 0.00, "change_reason": "Reason for change"}},
        "Category2": {{"proposed_change": 0.00, "change_reason": "Reason for change"}},
        ...
      }}
    }}
    ---BUDGET_JSON_END---

    Ensure that the total proposed budget matches the monthly income of ${user_data.current_income:.2f}.

    Base your advice on best practices from reputable financial sources such as {', '.join(sources)}.
    """

    if follow_up_question:
        prompt += f"\n\nFollow-up Question from the user: {follow_up_question}\n"
        prompt += """
        Please address this question in your response, providing additional advice or clarification as needed.
        IMPORTANT: Generate a new Proposed Monthly Budget that takes into account the follow-up question or comment.
        Ensure that this new budget is presented in the same JSON format as before, and that it still matches the monthly income exactly.
        Explain the changes made to the budget in response to the follow-up question.
        """

    return system_message, prompt

def get_top_expenses(bank_statement: List[BankStatementEntry]) -> str:
    expenses = {}
    for entry in bank_statement:
        if entry.Withdrawals > 0:
            expenses[entry.Category] = expenses.get(entry.Category, 0) + entry.Withdrawals
    
    sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_expenses[:5]
    
    return "\n".join([f"{category}: ${amount:.2f}" for category, amount in top_5])

def generate_advice_stream(user_data: UserDataInput, follow_up_question: str = None):
    print("generate_advice_stream function called")
    print(f"Generating advice for user with income: ${user_data.current_income:.2f}")
    try:
        sources = get_sources()
        system_message, gpt_prompt = create_gpt_prompt(user_data, sources, follow_up_question)
        
        print(f"GPT prompt created. Income in prompt: ${user_data.current_income:.2f}")
        print(f"Full GPT prompt: {gpt_prompt}")

        yield from call_llm_api(system_message, gpt_prompt, user_data.selected_llm)

    except Exception as e:
        print(f"Error in generate_advice_stream: {str(e)}")
        yield f"Error generating advice: {str(e)}"

def call_llm_api(system_message: str, prompt: str, model_name: str):
    if model_name == "GPT-4":
        yield from handle_gpt4(system_message, prompt)
    elif model_name in ["gpt2", "distilgpt2"]:
        try:
            response = handle_huggingface_model(prompt, model_name)
            yield response
        except Exception as e:
            yield f"Error processing {model_name}: {str(e)}"
    else:
        yield f"Unsupported model: {model_name}"

def get_advice(user_data: UserDataInput):
    print("get_advice function called")
    print(f"Generating advice for user with income: ${user_data.current_income:.2f}")
    try:
        user_context = prepare_user_context(user_data)
        if "error" in user_context:
            print(f"Error in user context: {user_context['error']}")
            yield f"Error: {user_context['error']}"
            return

        print(f"User context prepared. Income: ${float(user_context['income']):.2f}")

        sources = get_sources()
        system_message, gpt_prompt = create_gpt_prompt(user_data, sources)
        
        print(f"GPT prompt created. Income in prompt: ${float(user_context['income']):.2f}")
        print(f"Full GPT prompt: {gpt_prompt}")

        yield from call_llm_api(system_message, gpt_prompt, user_context['selected_llm'])

    except Exception as e:
        print(f"Error in get_advice: {str(e)}")
        yield f"Error generating advice: {str(e)}"

def format_constraints(constraints: Optional[List[str]]) -> str:
    if not constraints:
        return "No specific constraints provided."
    return "\n".join(f"- {constraint}" for constraint in constraints)
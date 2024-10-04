from typing import List, Dict, Tuple
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

def prepare_user_context(user_data: UserDataInput):
    logger.info(f"Preparing user context with income: ${user_data.current_income:.2f}")
    try:
        if isinstance(user_data.bank_statement, list):
            df = pd.DataFrame([entry.dict() for entry in user_data.bank_statement])
        elif isinstance(user_data.bank_statement, pd.DataFrame):
            df = user_data.bank_statement
        else:
            raise ValueError("Invalid bank statement format")

        required_columns = ['Date', 'Description', 'Category', 'Withdrawals']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [col for col in required_columns if col not in df.columns]
            logger.error(f"Missing columns in bank statement: {missing_columns}")
            return {
                "error": f"Bank statement data is missing columns: {', '.join(missing_columns)}"
            }

        df['Withdrawals'] = df['Withdrawals'].fillna(0.0).astype(float)

        total_expenses = df['Withdrawals'].sum()
        
        categorized_expenses = df.groupby('Category')['Withdrawals'].sum().to_dict()
        savings_rate = calculate_savings_rate(user_data.current_income, total_expenses)

        return {
            "name": user_data.name,
            "income": user_data.current_income,
            "expenses": total_expenses,
            "savings_rate": savings_rate,
            "goals": user_data.goals,
            "timeline": user_data.timeline_months,
            "age": user_data.age,
            "location": user_data.address,
            "categorized_expenses": categorized_expenses,
            "selected_llm": user_data.selected_llm  
        }

    except Exception as e:
        logger.exception("Error in prepare_user_context")
        return {
            "error": f"Error processing user data: {str(e)}"
        }

def create_gpt_prompt(user_data: UserDataInput, sources: List[str]) -> Tuple[str, str]:
    print(f"Creating prompt with income: ${user_data.current_income:.2f}")
    
    system_message = f"""You are a friendly, empathetic professional budget advisor. Provide a detailed yet approachable financial analysis and budgeting advice for the following client. Use a warm, first-person perspective as if you're having a conversation with a friend. The client's monthly income is EXACTLY ${user_data.current_income:.2f}. 
    Always use this exact income figure in your analysis and advice. Do not assume or use any other income figure."""
    
    prompt = f"""
    Based on the following user information and financial data, provide a comprehensive financial analysis and advice:

    Name: {user_data.name}
    Age: {user_data.age}
    Location: {user_data.address}
    Monthly Income: ${user_data.current_income:.2f}
    Current Savings: ${user_data.current_savings:.2f}
    Financial Goals: {', '.join(user_data.goals)}
    Timeline: {user_data.timeline_months} months

    Bank Statement Summary:
    Total Withdrawals: ${sum(entry.Withdrawals for entry in user_data.bank_statement):.2f}

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

    return system_message, prompt

def get_top_expenses(bank_statement: List[BankStatementEntry]) -> str:
    expenses = {}
    for entry in bank_statement:
        if entry.Withdrawals > 0:
            expenses[entry.Category] = expenses.get(entry.Category, 0) + entry.Withdrawals
    
    sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_expenses[:5]
    
    return "\n".join([f"{category}: ${amount:.2f}" for category, amount in top_5])

def generate_advice_stream(user_data: UserDataInput):
    print("generate_advice_stream function called")
    print(f"Generating advice for user with income: ${user_data.current_income:.2f}")
    try:
        user_context = prepare_user_context(user_data)
        if "error" in user_context:
            print(f"Error in user context: {user_context['error']}")
            yield f"Error: {user_context['error']}"
            return

        print(f"User context prepared. Income: ${float(user_context['income']):.2f}")

        sources = get_sources()
        system_message, prompt = create_gpt_prompt(user_data, sources)
        
        print(f"GPT prompt created. Income in prompt: ${float(user_context['income']):.2f}")
        print(f"Full GPT prompt: {prompt}")

        yield from call_llm_api(system_message, prompt, user_context['selected_llm'])

    except Exception as e:
        print(f"Error in generate_advice_stream: {str(e)}")
        yield f"Error: {str(e)}"

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
        system_message, gpt_prompt = create_gpt_prompt(user_context, sources)
        
        print(f"GPT prompt created. Income in prompt: ${float(user_context['income']):.2f}")
        print(f"Full GPT prompt: {gpt_prompt}")

        yield from call_llm_api(system_message, gpt_prompt, user_context['selected_llm'])

    except Exception as e:
        print(f"Error in get_advice: {str(e)}")
        yield f"Error generating advice: {str(e)}"
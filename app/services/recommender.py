from typing import List, Dict
from app.api.models import UserDataInput
from app.core.config import get_sources
from dotenv import load_dotenv
import torch
import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from .model_handlers import handle_huggingface_model, handle_gpt4
import pandas as pd

# Replace the existing logging setup with this:
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

        required_columns = ['Date', 'Description', 'Category', 'Withdrawals', 'Deposits']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [col for col in required_columns if col not in df.columns]
            logger.error(f"Missing columns in bank statement: {missing_columns}")
            return {
                "error": f"Bank statement data is missing columns: {', '.join(missing_columns)}"
            }

        df['Withdrawals'] = df['Withdrawals'].fillna(0.0).astype(float)
        df['Deposits'] = df['Deposits'].fillna(0.0).astype(float)

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

def create_gpt_prompt(user_context: Dict, sources: List[str]) -> str:
    print(f"Creating prompt with income: ${float(user_context['income']):.2f}")
    print(f"User context in create_gpt_prompt: {user_context}")
    print(f"Income type: {type(user_context['income'])}")
    print(f"Income value: {user_context['income']}")
    
    system_message = f"""    You are a friendly, empathetic professional budget advisor. Provide a detailed yet approachable financial analysis and budgeting advice for the following client. Use a warm, first-person perspective as if you're having a conversation with a friend. The client's monthly income is EXACTLY ${float(user_context['income']):.2f}. 
    Always use this exact income figure in your analysis and advice. Do not assume or use any other income figure."""
    
    prompt = f"""
    Based on the following user information and financial data, provide a comprehensive financial analysis and advice:

    Name: {user_context['name']}
    Age: {user_context['age']}
    Location: {user_context['address']}
    Monthly Income: ${float(user_context['income']):.2f}
    Current Savings: ${float(user_context['current_savings']):.2f}
    Financial Goals: {', '.join(user_context['goals'])}
    Timeline: {user_context['timeline_months']} months

    Bank Statement Summary:
    Total Deposits: ${float(user_context['total_deposits']):.2f}
    Total Withdrawals: ${float(user_context['total_withdrawals']):.2f}

    Top Expense Categories:
    {user_context['top_expenses']}

    IMPORTANT: The client's monthly income is EXACTLY ${float(user_context['income']):.2f}. Do not use any other income figure in your analysis or advice. This is the correct and only income figure to use.
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

    Ensure that the total proposed budget matches the monthly income of ${float(user_context['income']):.2f}.

    Base your advice on best practices from reputable financial sources such as {', '.join(sources)}.
    """

    return system_message, prompt

def generate_advice_stream(user_data: UserDataInput):
    print("generate_advice_stream function called")
    print(f"Generating advice for user with income: ${user_data.current_income:.2f}")
    try:
        print(f"Original user data income: {user_data.current_income}")
        user_context = prepare_user_context(user_data)
        if "error" in user_context:
            print(f"Error in user context: {user_context['error']}")
            yield f"Error: {user_context['error']}"
            return

        print(f"User context prepared. Income: ${float(user_context['income']):.2f}")

        sources = get_sources()
        gpt_prompt = create_gpt_prompt(user_context, sources)
        
        print(f"GPT prompt created. Income in prompt: ${float(user_context['income']):.2f}")
        print(f"Full GPT prompt: {gpt_prompt}")

        yield from call_llm_api(gpt_prompt, user_context['selected_llm'])

    except Exception as e:
        print(f"Error in generate_advice_stream: {str(e)}")
        yield f"Error generating advice: {str(e)}"

def call_llm_api(prompt: str, model_name: str, timeout: int = 10):
    if model_name == "GPT-4":
        yield from handle_gpt4(prompt)
    elif model_name in ["gpt2", "distilgpt2"]:
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(handle_huggingface_model, prompt, model_name)
                try:
                    result = future.result(timeout=timeout)
                    required_keywords = ["Income and Expense Analysis", "Savings Rate Evaluation", "Goal Feasibility", "Recommendations"]
                    if len(result) < 200 or not all(keyword in result for keyword in required_keywords):
                        print(f"Inadequate response from {model_name}. Falling back to GPT-4.")
                        yield from handle_gpt4(prompt)
                    else:
                        yield result
                except TimeoutError:
                    print(f"Timeout reached for {model_name}. Falling back to GPT-4.")
                    yield from handle_gpt4(prompt)
        except Exception as e:
            print(f"Error with {model_name}: {str(e)}. Falling back to GPT-4.")
            yield from handle_gpt4(prompt)
    else:
        print(f"Unsupported model: {model_name}. Using GPT-4.")
        yield from handle_gpt4(prompt)

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
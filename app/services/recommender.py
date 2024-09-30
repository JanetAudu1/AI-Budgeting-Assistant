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

def prepare_user_context(user_data: UserDataInput):
    try:
        if isinstance(user_data.bank_statement, list):
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame([entry.dict() for entry in user_data.bank_statement])
        elif isinstance(user_data.bank_statement, pd.DataFrame):
            df = user_data.bank_statement
        else:
            raise ValueError("Invalid bank statement format")

        logger.info(f"Bank statement columns: {df.columns}")
        logger.info(f"Bank statement data types: {df.dtypes}")
        logger.info(f"First few rows of bank statement: {df.head().to_dict()}")

        required_columns = ['Date', 'Description', 'Category', 'Withdrawals', 'Deposits']
        if not all(col in df.columns for col in required_columns):
            missing_columns = [col for col in required_columns if col not in df.columns]
            logger.error(f"Missing columns in bank statement: {missing_columns}")
            return {
                "error": f"Bank statement data is missing columns: {', '.join(missing_columns)}"
            }

        # Convert Withdrawals and Deposits to float, replacing None with 0.0
        df['Withdrawals'] = df['Withdrawals'].fillna(0.0).astype(float)
        df['Deposits'] = df['Deposits'].fillna(0.0).astype(float)

        total_expenses = df['Withdrawals'].sum()
        total_income = df['Deposits'].sum()
        
        categorized_expenses = df.groupby('Category')['Withdrawals'].sum().to_dict()
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
            "categorized_expenses": categorized_expenses,
            "selected_llm": user_data.selected_llm  
        }

    except Exception as e:
        logger.exception("Error in prepare_user_context")
        return {
            "error": f"Error processing user data: {str(e)}"
        }

def create_gpt_prompt(user_context: Dict, sources: List[str]) -> str:
    return f"""
    You are a friendly, empathetic professional budget advisor. Provide a detailed yet approachable financial analysis and budgetingadvice for the following client. Use a warm, first-person perspective as if you're having a conversation with a friend:
    
    Client Information:
    - Name: {user_context['name']}
    - Age: {user_context['age']}
    - Location: {user_context['location']}
    - Monthly Income: ${float(user_context['income']):.2f}
    - Monthly Expenses: ${float(user_context['expenses']):.2f}
    - Current Savings Rate: {float(user_context['savings_rate']):.2f}%
    - Financial Goals: {', '.join(user_context['goals'])}

    Expense Breakdown:
    {', '.join([f'- {category}: ${float(amount):.2f}' for category, amount in user_context['categorized_expenses'].items()])}

    Please provide your analysis and advice in the following format:

    1. Income and Expense Analysis:
    [Provide a brief analysis of the client's income and expenses]

    2. Savings Rate Evaluation:
    [Evaluate the client's current savings rate]

    3. Goal Feasibility:
    [Assess the feasibility of each of the client's financial goals]

    4. Recommendations:
    [Provide specific, actionable recommendations to improve the client's financial situation]

    5. Conclusion:
    [Summarize your advice and provide encouragement to the client]

    Remember to be friendly, use "I" statements, and provide advice based on sound financial principles.

    After your analysis, please include a JSON representation of the proposed monthly budget using the following format:

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

    Replace [Total income], [Amount], and [Proposed savings amount] with actual numerical values based on your recommendations.
    """

def generate_advice_stream(user_data: UserDataInput):
    try:
        user_context = prepare_user_context(user_data)
        if "error" in user_context:
            yield f"Error: {user_context['error']}"
            return

        sources = get_sources()
        gpt_prompt = create_gpt_prompt(user_context, sources)
        
        yield from call_llm_api(gpt_prompt, user_context['selected_llm'])

    except Exception as e:
        logger.exception("Error in generate_advice_stream")
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
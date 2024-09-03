import os
import quandl
from typing import List, Dict
from data_validation import UserData

# Set Quandl API key
quandl.ApiConfig.api_key = 'QUANDL_API_KEY'

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
                
                # Check if the amount_str is not empty
                if amount_str:
                    try:
                        amount = float(amount_str.replace('+', '').replace('-', '').replace(',', ''))
                    except ValueError:
                        # Skip lines where the amount cannot be converted to float
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

def get_gdp_data():
    """Fetches the latest U.S. GDP data from Quandl."""
    try:
        gdp_data = quandl.get("FRED/GDP")
        latest_gdp = gdp_data.tail(1).values[0][0]
        return latest_gdp
    except Exception as e:
        return None

def generate_advice(user_data: UserData, sources: str) -> str:
    try:
        # Fetch economic data from Quandl
        latest_gdp = get_gdp_data()
        
        # Unpack bank statement data
        total_income, total_expenses, categorized_expenses = parse_bank_statement(user_data.bank_statement)

        # Calculate savings rate
        savings_rate = calculate_savings_rate(total_income, total_expenses)

        # Customize advice based on priorities
        advice = []
        advice.append(f"Hi {user_data.name}, based on your financial data and the latest economic trends, here's what we suggest:")

        # Incorporate GDP data into the advice
        if latest_gdp:
            advice.append(f"- **Economic Outlook**: The latest U.S. GDP is {latest_gdp:.2f} trillion USD. This reflects the current economic growth, which could impact your investment strategies.")

        # Savings Advice
        if "savings" in user_data.priorities:
            advice.append(f"- **Savings**: You're currently saving {savings_rate:.2f}% of your income. To reach your goal of saving ${user_data.savings_goal}, consider cutting back on discretionary expenses by ${0.1 * total_income:.2f} per month.")
        
        # Investment Advice
        if "investments" in user_data.priorities:
            investment_amount = 0.2 * user_data.current_savings
            advice.append(f"- **Investments**: Consider investing ${investment_amount:.2f} of your savings into low-risk index funds, which could grow to ${investment_amount * 1.5:.2f} over the next 5 years based on average returns.")

        # Debt Repayment Advice
        if "debt repayment" in user_data.priorities:
            debt_repayment = 0.3 * user_data.current_income
            advice.append(f"- **Debt Repayment**: Prioritize paying down high-interest debt. If you allocate ${debt_repayment:.2f} per month, you could save ${debt_repayment * 0.15:.2f} in interest over the next year.")

        # Location-Based Adjustments
        advice.append(f"Since you're living in {user_data.address}, where the cost of living index is X, it’s important to budget accordingly. Make sure your budget reflects these higher costs.")

        # Add more personalized advice based on additional priorities
        if "retirement" in user_data.priorities:
            advice.append(f"- **Retirement**: Based on your age ({user_data.age}), it's a great time to start or continue contributing to your retirement savings. Consider contributing to a 401(k) or IRA if you haven't already.")

        advice.append(f"\nKeep these strategies in mind as you work towards your financial goals. Every small step adds up!")
        
        return "\n".join(advice)

    except Exception as e:
        raise Exception(f"Error generating financial advice: {str(e)}")


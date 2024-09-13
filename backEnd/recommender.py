import os
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

def generate_advice(user_data: UserData, sources: str) -> str:
    try:
        # Unpack bank statement data
        total_income, total_expenses, categorized_expenses = parse_bank_statement(user_data.bank_statement)

        # Calculate savings rate
        savings_rate = calculate_savings_rate(total_income, total_expenses)

        # Begin crafting advice
        advice = []
        advice.append(f"Hi {user_data.name}, here’s a snapshot of your current financial situation based on your recent bank statement:")

        # Income and Expense Overview
        advice.append(f"- **Total Income**: You've earned ${total_income:.2f} this month.")
        advice.append(f"- **Total Expenses**: You've spent ${total_expenses:.2f}, broken down as follows:")
        for category, amount in categorized_expenses.items():
            percentage = (amount / total_expenses) * 100 if total_expenses else 0
            advice.append(f"  - {category.capitalize()}: ${amount:.2f} ({percentage:.2f}% of total expenses)")

        # Savings Rate
        advice.append(f"- **Savings Rate**: You're saving {savings_rate:.2f}% of your income.")
        
        # Savings Goal Calculation
        if "savings" in user_data.priorities:
            amount_needed = user_data.savings_goal - (total_income - total_expenses)
            monthly_savings_goal = amount_needed / 12  # Assuming an annual goal
            advice.append(f"- **Savings Goal**: You need to save ${monthly_savings_goal:.2f} per month to reach your goal of saving ${user_data.savings_goal:.2f} in the next year.")
        
        # Investment Advice
        if "investments" in user_data.priorities:
            recommended_investment = 0.2 * (total_income - total_expenses)
            advice.append(f"- **Investment Suggestion**: Based on your current savings, you could invest ${recommended_investment:.2f} this month into low-risk options like index funds.")

        # Debt Repayment Suggestion
        if "debt repayment" in user_data.priorities:
            debt_repayment_amount = 0.3 * total_income
            advice.append(f"- **Debt Repayment**: To reduce high-interest debt, allocate ${debt_repayment_amount:.2f} per month. Over a year, this could save you around ${debt_repayment_amount * 0.15:.2f} in interest.")

        advice.append(f"\nKeep up the good work! Making these small adjustments can help you meet your financial goals faster. Feel free to revisit your priorities each month to see how you're progressing.")

        return "\n".join(advice)

    except Exception as e:
        raise Exception(f"Error generating financial advice: {str(e)}")


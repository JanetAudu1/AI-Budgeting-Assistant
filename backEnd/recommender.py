from data_validation import UserData  # Import the UserData model
from fastapi import HTTPException  # For raising HTTP exceptions in FastAPI

def parse_bank_statement(bank_statement: str) -> dict:
    """Parse the bank statement and extract financial data."""
    lines = bank_statement.strip().splitlines()
    total_income = 0
    total_expenses = 0
    major_expenses = []

    for line in lines:
        if '|' in line and 'Date' not in line and 'Transactions' not in line:
            parts = [part.strip() for part in line.split('|')]
            if len(parts) >= 3:
                description = parts[1]
                amount_str = parts[2]
                if amount_str.startswith('+'):
                    amount = float(amount_str.replace('+', '').replace(',', ''))
                    total_income += amount
                elif amount_str.startswith('-'):
                    amount = float(amount_str.replace('-', '').replace(',', ''))
                    total_expenses += amount
                    major_expenses.append((description, amount))

    savings_rate = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings_rate": savings_rate,
        "major_expenses": major_expenses
    }

def get_financial_advice(user_data: UserData, sources: str) -> str:
    """Generate personalized budgeting advice based on user data."""
    try:
        bank_data = parse_bank_statement(user_data.bank_statement)

        advice = []

        # Total income and expenses
        total_income = bank_data['total_income']
        total_expenses = bank_data['total_expenses']

        # Calculate monthly savings rate
        if total_income > 0:
            monthly_savings_rate = ((total_income - total_expenses) / total_income) * 100
            advice.append(f"Your current savings rate is {monthly_savings_rate:.2f}%.")
        else:
            advice.append("No income detected in your bank statement, so a savings rate cannot be calculated.")

        # Essential vs Discretionary Spending
        essential_expenses = sum([amount for desc, amount in bank_data['major_expenses'] if desc in ['Rent', 'Utilities', 'Groceries']])
        discretionary_expenses = total_expenses - essential_expenses
        
        advice.append(f"Your essential expenses (Rent, Utilities, Groceries) total ${essential_expenses:.2f}. "
                      f"Your discretionary spending totals ${discretionary_expenses:.2f}. "
                      "Consider keeping discretionary spending under control to boost your savings rate.")

        # Customized Recommendations
        if user_data.priorities:
            for priority in user_data.priorities:
                if priority.lower() == "savings":
                    advice.append("Consider automating transfers to a savings account right after you receive your paycheck to prioritize your savings.")
                elif priority.lower() == "investments":
                    if monthly_savings_rate > 0:
                        advice.append("Given your savings rate, consider allocating a portion of your income towards investments, focusing on low-risk, long-term options.")
                    else:
                        advice.append("Before focusing on investments, ensure that you have a positive savings rate.")
                elif priority.lower() == "debt repayment":
                    advice.append("Prioritize paying down any existing debts, especially high-interest ones, to free up more of your income for savings and investments.")
                elif priority.lower() == "budget optimization":
                    advice.append("Review your spending in discretionary categories, such as dining out or subscriptions, and identify areas to cut back.")

        # Location-based adjustments
        if "New York" in user_data.address:
            advice.append("Living in New York means higher living costs; ensure your budget accounts for higher rent and transportation costs.")
        elif "California" in user_data.address:
            advice.append("In California, consider allocating more towards savings due to the state's high living costs and taxes.")

        # Closing Advice
        advice.append("Regularly review your budget and adjust your spending and savings goals to reflect changes in income or expenses.")

        formatted_advice = "\n\n".join(advice)

        return formatted_advice

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating financial advice: {str(e)}")


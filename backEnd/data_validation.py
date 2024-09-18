from dataclasses import dataclass, field
from typing import List
import pandas as pd

@dataclass
class UserData:
    """
    A class to represent user financial data with built-in validation.

    This class stores and validates various pieces of financial information
    provided by the user, including personal details, financial goals, and
    bank statement data.

    Attributes:
        name (str): The user's name.
        age (int): The user's age.
        address (str): The user's address.
        current_income (float): The user's current monthly income.
        current_savings (float): The user's current savings.
        goals (List[str]): A list of the user's financial goals.
        timeline_months (int): The timeline for financial goals in months.
        bank_statement (pd.DataFrame): The user's bank statement as a pandas DataFrame.
        priorities (List[str]): A list of the user's financial priorities.
        savings_goal (float): The user's savings goal amount.
    """

    name: str
    age: int
    address: str
    current_income: float
    current_savings: float
    goals: List[str]
    timeline_months: int
    bank_statement: pd.DataFrame
    priorities: List[str]
    savings_goal: float
    validation_errors: List[str] = field(default_factory=list)

    def validate(self):
        """
        Validate all attributes of the UserData object.
        
        Returns:
            bool: True if all validations pass, False otherwise.
        """
        self.validation_errors = []
        
        self._validate_string(self.name, "Name")
        self._validate_numeric(self.age, 18, 120, "Age")
        self._validate_string(self.address, "Address")
        self._validate_numeric(self.current_income, 0.01, 1000000, "Current Monthly Income")
        self._validate_numeric(self.current_savings, 0, 10000000, "Current Savings")
        self._validate_list(self.goals, "Goals")
        self._validate_numeric(self.timeline_months, 1, 600, "Timeline")
        self._validate_list(self.priorities, "Priorities")
        self._validate_numeric(self.savings_goal, 0.01, 10000000, "Savings Goal")
        
        return len(self.validation_errors) == 0

    def _validate_string(self, value, field_name):
        if not isinstance(value, str) or not value.strip():
            self.validation_errors.append(f"{field_name} must be a non-empty string.")

    def _validate_numeric(self, value, min_value, max_value, field_name):
        if not isinstance(value, (int, float)):
            self.validation_errors.append(f"{field_name} must be a number.")
        elif value < min_value or value > max_value:
            self.validation_errors.append(f"{field_name} must be between {min_value} and {max_value}.")

    def _validate_list(self, value, field_name):
        if not isinstance(value, list) or not value:
            self.validation_errors.append(f"{field_name} must be a non-empty list.")

    def validate_bank_statement(self):
        """
        Validate the bank statement DataFrame.
        
        Returns:
            bool: True if validation passes, False otherwise.
        """
        if not isinstance(self.bank_statement, pd.DataFrame):
            self.validation_errors.append("Bank statement must be a pandas DataFrame.")
            return False
        
        required_columns = ['Date', 'Description', 'Category', 'Withdrawals', 'Deposits']
        missing_columns = [col for col in required_columns if col not in self.bank_statement.columns]
        
        if missing_columns:
            self.validation_errors.append(f"Bank statement is missing required columns: {', '.join(missing_columns)}")
            return False
        
        return True

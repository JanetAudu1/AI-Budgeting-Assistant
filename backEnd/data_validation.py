from typing import List
from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    age: int
    address: str
    current_income: float
    current_savings: float
    goals: List[str]
    timeline_months: int
    bank_statement: str
    priorities: List[str]
    savings_goal: float

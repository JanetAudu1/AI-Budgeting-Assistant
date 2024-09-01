from pydantic import BaseModel
from typing import List

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


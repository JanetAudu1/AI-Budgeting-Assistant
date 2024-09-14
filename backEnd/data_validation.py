from typing import List
from pydantic import BaseModel
import pandas as pd

class UserData(BaseModel):
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

    class Config:
        arbitrary_types_allowed = True

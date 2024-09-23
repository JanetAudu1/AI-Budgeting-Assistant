from pydantic import BaseModel
from typing import List, Optional

class UserDataInput(BaseModel):
    name: str
    age: int
    address: str
    current_income: float
    current_savings: float
    goals: List[str]
    timeline_months: int
    bank_statement: List[dict]

    class Config:
        arbitrary_types_allowed = True

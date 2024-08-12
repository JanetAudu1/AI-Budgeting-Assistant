from pydantic import BaseModel, Field
from typing import List

class UserData(BaseModel):
    name: str = Field(..., description="User's name")
    age: int = Field(..., gt=0, description="User's age must be a positive integer")
    address: str = Field(..., description="User's address")
    current_income: float = Field(..., gt=0, description="Current monthly income")
    current_savings: float = Field(..., ge=0, description="Current savings")
    goals: List[str] = Field(..., description="List of financial goals")
    timeline_months: int = Field(..., gt=0, description="Timeline to achieve goals in months")
    bank_statement: str = Field(..., description="User's bank statement content as a string")


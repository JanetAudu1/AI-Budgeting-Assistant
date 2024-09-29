from pydantic import BaseModel, validator, Field
from typing import List, Optional
import pandas as pd
from datetime import date

class BankStatementEntry(BaseModel):
    Date: date
    Description: str
    Category: str
    Withdrawals: Optional[float] = None
    Deposits: Optional[float] = None

class UserDataInput(BaseModel):
    name: str
    age: int = Field(..., ge=18, le=120)
    address: str
    current_income: float = Field(..., gt=0, le=1000000)
    current_savings: float = Field(..., ge=0, le=10000000)
    goals: List[str]
    timeline_months: int = Field(..., ge=1, le=600)
    bank_statement: List[BankStatementEntry]
    selected_llm: str

    @validator('name', 'address')
    def validate_non_empty_string(cls, v):
        if not v.strip():
            raise ValueError("Must be a non-empty string")
        return v

    @validator('goals')
    def validate_non_empty_list(cls, v):
        if not v:
            raise ValueError("Must be a non-empty list")
        return v

    @validator('bank_statement')
    def validate_bank_statement(cls, v):
        if not v:
            raise ValueError("Bank statement must not be empty")
        
        df = pd.DataFrame([entry.dict() for entry in v])
        required_columns = ['Date', 'Description', 'Category', 'Withdrawals', 'Deposits']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Bank statement is missing required columns: {', '.join(missing_columns)}")
        
        return v

    def to_dict(self):
        def clean_float(value):
            if isinstance(value, float):
                return None if pd.isna(value) or pd.isinf(value) else round(value, 2)
            return value

        data = self.dict()
        data['bank_statement'] = [entry.dict() for entry in self.bank_statement]
        
        for entry in data['bank_statement']:
            entry.update({k: clean_float(v) for k, v in entry.items() if isinstance(v, float)})
        
        data.update({k: clean_float(v) for k, v in data.items() if isinstance(v, float)})
        
        return data

    class Config:
        arbitrary_types_allowed = True

__all__ = ['UserDataInput', 'BankStatementEntry']
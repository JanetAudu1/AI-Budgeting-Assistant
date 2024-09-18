import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
import logging
from backEnd.data_validation import UserData
from backEnd.recommender import generate_advice_stream

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdviceResponse(BaseModel):
    advice: str

class UserDataModel(BaseModel):
    name: str
    age: int
    address: str
    current_income: Optional[float] = Field(None)
    current_savings: Optional[float] = Field(None)
    goals: List[str]
    timeline_months: int
    bank_statement: List[dict]
    savings_goal: Optional[float] = Field(None)
    priorities: Optional[List[str]] = None
    debt: Optional[float] = Field(None)
    debt_repayment_goal: Optional[float] = Field(None)

    class Config:
        arbitrary_types_allowed = True

@app.post("/get_advice")
async def get_advice(user_data: UserDataModel):
    try:
        # Convert bank_statement back to DataFrame if needed
        bank_statement_df = pd.DataFrame(user_data.bank_statement)
        
        # Create UserData object
        user_data_obj = UserData(
            name=user_data.name,
            age=user_data.age,
            address=user_data.address,
            current_income=user_data.current_income or 0.0,
            current_savings=user_data.current_savings or 0.0,
            goals=user_data.goals,
            timeline_months=user_data.timeline_months,
            bank_statement=bank_statement_df,
            savings_goal=user_data.savings_goal or 0.0,
            priorities=user_data.priorities,
            debt=user_data.debt,
            debt_repayment_goal=user_data.debt_repayment_goal
        )

        # Generate advice using the existing generate_advice_stream function
        return StreamingResponse(generate_advice_stream(user_data_obj), media_type="text/plain")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating advice: {str(e)}")


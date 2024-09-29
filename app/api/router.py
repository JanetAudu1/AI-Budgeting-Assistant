from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from app.api.models import UserDataInput, UserData
from app.core.data_validation import UserData as CoreUserData
import pandas as pd

router = APIRouter()

@router.post("/generate-advice")
async def generate_advice(user_data_input: UserDataInput):
    # Convert UserDataInput to CoreUserData
    user_data = CoreUserData(
        name=user_data_input.name,
        age=user_data_input.age,
        address=user_data_input.address,
        current_income=user_data_input.current_income,
        current_savings=user_data_input.current_savings,
        goals=user_data_input.goals,
        timeline_months=user_data_input.timeline_months,
        bank_statement=user_data_input.bank_statement,
        selected_llm=user_data_input.selected_llm
    )

    # Perform additional validation
    if not user_data.validate():
        return JSONResponse(content={"errors": user_data.validation_errors}, status_code=400)


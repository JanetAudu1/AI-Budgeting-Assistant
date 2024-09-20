from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from app.api.models import UserDataInput
from app.core.data_validation import UserData
from app.services.recommender import generate_advice_stream
import pandas as pd
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/get_advice")
async def get_advice(user_data_input: UserDataInput) -> StreamingResponse:
    logger.info(f"Received request for user: {user_data_input.name}")
    
    # Convert UserDataInput to UserData
    user_data = UserData(
        name=user_data_input.name,
        age=user_data_input.age,
        address=user_data_input.address,
        current_income=user_data_input.current_income,
        current_savings=user_data_input.current_savings,
        goals=user_data_input.goals,
        timeline_months=user_data_input.timeline_months,
        bank_statement=pd.DataFrame(user_data_input.bank_statement),
        priorities=user_data_input.priorities
    )
    
    if user_data.validate() and user_data.validate_bank_statement():
        logger.info(f"Validation successful for user: {user_data.name}")
        return StreamingResponse(generate_advice_stream(user_data), media_type="text/event-stream")
    else:
        logger.error(f"Validation failed for user: {user_data.name}. Errors: {user_data.validation_errors}")
        return JSONResponse(status_code=400, content={"errors": user_data.validation_errors})

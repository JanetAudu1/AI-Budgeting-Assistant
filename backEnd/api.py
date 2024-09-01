from fastapi import FastAPI, HTTPException, Depends
from recommender import get_financial_advice
from data_validation import UserData
from config import get_sources
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/get_advice")
def get_advice(user_data: UserData):
    try:
        logger.info(f"Received request for user: {user_data.name}")

        sources = get_sources()
        advice = get_financial_advice(user_data, sources)

        return {"advice": advice}

    except HTTPException as e:
        logger.error(f"Error processing request: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


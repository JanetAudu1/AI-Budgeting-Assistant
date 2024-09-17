import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Depends
from recommender import generate_advice_stream 
from data_validation import UserData
from config import get_sources
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/get_advice")
def get_advice(user_data: UserData):
    """
    FastAPI endpoint for generating financial advice.
    
    This function receives user data, logs the request, fetches financial sources,
    and generates personalized financial advice.
    
    Args:
    user_data (UserData): The user's financial data and goals.
    
    Returns:
    dict: A dictionary containing the generated advice.
    
    Raises:
    HTTPException: If there's an error in processing the request or generating advice.
    """
    try:
        logger.info(f"Received request for user: {user_data.name}")

        sources = get_sources()
        logger.info(f"Fetching financial advice for {user_data.name} using sources: {sources}")

        advice = generate_advice_stream(user_data, sources)

        return {"advice": advice}

    except HTTPException as e:
        logger.error(f"HTTP error processing request: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


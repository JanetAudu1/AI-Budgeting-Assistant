from fastapi import FastAPI, HTTPException, Depends
from recommender import get_financial_advice, format_advice_to_table
from data_validation import UserData
from config import get_sources  # Import the dynamic sources function
import logging

# Initialize the FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency injection
def get_user_data(user_data: UserData = Depends()) -> UserData:
    """Validate and provide user data as a dependency."""
    return user_data

# Define the FastAPI endpoint
@app.post("/get_advice")
def get_advice(user_data: UserData = Depends(get_user_data)):
    """Endpoint to get financial advice based on user data."""
    try:
        logger.info(f"Received request for user: {user_data.name}")
        
        sources = get_sources()  # Fetch dynamic sources
        advice = get_financial_advice(user_data, sources)
        formatted_advice = format_advice_to_table(advice, sources)
        
        return {"advice": formatted_advice}
    
    except HTTPException as e:
        logger.error(f"Error processing request: {str(e)}")
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Entry point for running the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


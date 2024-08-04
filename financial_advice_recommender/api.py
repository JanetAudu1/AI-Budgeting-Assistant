from fastapi import FastAPI, HTTPException
from data_validation import UserData
from recommender import get_financial_advice, format_advice_to_table

# Initialize the FastAPI app
app = FastAPI()

# Define the FastAPI endpoint
@app.post("/get_advice")
def get_advice(user_data: UserData):
    try:
        advice = get_financial_advice(user_data)
        sources = "Advice generated using GPT-3.5-turbo and validated financial principles from sources such as Investopedia, NerdWallet, and Financial Times."
        formatted_advice = format_advice_to_table(advice, sources)
        return {"advice": formatted_advice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Entry point for running the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


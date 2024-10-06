"""
FastAPI main application file for the AI Budgeting Assistant.

This file sets up the FastAPI application, defines API routes,
and handles the generation of financial advice through a
streaming response.
"""

import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.api.models import UserDataInput
from app.services.recommender import generate_advice_stream

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Budgeting Assistant API"}

@app.post("/get_advice")
async def get_advice(user_data: UserDataInput):
    return StreamingResponse(generate_advice_stream(user_data), media_type="text/plain")
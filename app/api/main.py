import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from app.api.router import router

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Budgeting Assistant API"}

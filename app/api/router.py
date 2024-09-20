from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from .models import UserDataModel, AdviceResponse
from app.core.data_validation import UserData
from app.services.recommender import generate_advice_stream

router = APIRouter()

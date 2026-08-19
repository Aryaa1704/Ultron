from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv("/workspaces/Ultron/.env")

from backend.database import get_session
from backend.auth import get_current_user
from backend.models import User
from pydantic import BaseModel

router = APIRouter()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction="You are JARVIS, an advanced AI Operating System. Be helpful, professional and proactive."
            )
        )
        return {
            "message": response.text,
            "agent_used": "gemini-brain",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

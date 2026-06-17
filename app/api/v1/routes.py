from fastapi import APIRouter

from app.schemas.chat import ChatRequest
from app.agents.flight import Flight

router = APIRouter()

assistant = Flight()


@router.post("/chat")
async def chat(request: ChatRequest):

    response = assistant.chat(
        request.message,
        []
    )

    return {
        "response": response
    }
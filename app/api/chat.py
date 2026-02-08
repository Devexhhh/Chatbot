from fastapi import APIRouter
from pydantic import BaseModel

from chatbot.ml_model import predict, get_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    intent = predict(req.message)
    reply = get_response(intent)
    return {"response": reply}

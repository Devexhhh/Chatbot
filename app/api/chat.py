from fastapi import APIRouter
from pydantic import BaseModel

from chatbot.ml_model import predict, get_response
from app.memory import get_memory, update_memory

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str   # NEW

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    memory = get_memory(req.user_id)

    intent, confidence = predict(req.message)

    # Handle vague replies using memory
    if confidence < 0.45:
        if "last_intent" in memory:
            reply = f"You were asking about **{memory['last_intent']}** earlier. Can you clarify?"
            return {"response": reply}

        return {"response": "I'm not sure I understood 🤔 Can you rephrase?"}

    # Save memory
    update_memory(req.user_id, {
        "last_intent": intent
    })

    reply = get_response(intent)
    return {"response": reply}

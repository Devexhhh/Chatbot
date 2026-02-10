from fastapi import APIRouter
from pydantic import BaseModel

from chatbot.ml_model import predict, get_response
from app.memory import get_memory, update_memory
from chatbot.skill_router import handle_skills

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str   # NEW

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # 1️⃣ Try skill-based handlers first (math, time, etc.)
    skill_response = handle_skills(req.message)
    if skill_response:
        return {"response": skill_response}

    # 2️⃣ Load user memory
    memory = get_memory(req.user_id)

    # 3️⃣ ML intent detection
    intent, confidence = predict(req.message)

    # 4️⃣ Low-confidence handling with memory
    if confidence < 0.45:
        if "last_intent" in memory:
            return {
                "response": f"You were asking about {memory['last_intent']} earlier. Can you clarify?"
            }

        return {"response": "I'm not sure I understood 🤔 Can you rephrase?"}

    # 5️⃣ Update memory
    update_memory(req.user_id, {
        "last_intent": intent
    })

    # 6️⃣ Normal response
    reply = get_response(intent)
    return {"response": reply}


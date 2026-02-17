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
async def chat(req: ChatRequest):

    # 1. Skills first
    skill_response = await handle_skills(req.message)
    if skill_response:
        return {"response": skill_response}

    # 2. Load memory
    memory = get_memory(req.user_id)

    # 3. Predict intent
    intent, confidence = predict(req.message)

    # 4. Save intent even if medium confidence
    if confidence >= 0.30:
        update_memory(req.user_id, {
            "last_intent": intent
        })

    # 5. Handle low confidence using memory
    if confidence < 0.45:
        if "last_intent" in memory:
            return {
                "response": f"You were asking about {memory['last_intent']} earlier. Can you clarify?"
            }

        return {"response": "I'm not sure I understood 🤔 Can you rephrase?"}

    # 6. Normal response
    reply = get_response(intent)
    return {"response": reply}



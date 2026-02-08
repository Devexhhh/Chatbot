from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI(title="AI chatbot API")

app.include_router(chat_router)

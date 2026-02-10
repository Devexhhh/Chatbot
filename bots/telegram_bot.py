import os
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

if not BOT_TOKEN or not API_URL:
    raise RuntimeError("Missing BOT_TOKEN or API_URL")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = str(update.message.from_user.id)

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            API_URL,
            json={
                "message": user_text,
                "user_id": user_id
            }
        )

    await update.message.reply_text(response.json()["response"])

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

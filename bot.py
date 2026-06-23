import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
ASSISTANT_HOST = os.getenv("ASSISTANT_HOST", "https://prod-1-data.ke.pinecone.io")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "argos")
MODEL = os.getenv("MODEL", "claude-3-5-sonnet")

client = OpenAI(
    api_key=PINECONE_API_KEY,
    base_url=f"{ASSISTANT_HOST}/assistant/chat/{ASSISTANT_NAME}"
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pregunta = update.message.text
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": pregunta}]
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("Argos Telegram -> Pinecone 24/7 iniciado")
    app.run_polling()

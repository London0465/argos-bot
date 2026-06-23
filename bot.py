import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

TOKEN = os.getenv("TELEGRAM_TOKEN")
PC_KEY = os.getenv("PINECONE_API_KEY")
ASSISTANT = os.getenv("ASSISTANT_NAME", "argos")
HOST = os.getenv("ASSISTANT_HOST", "https://prod-1-data.ke.pinecone.io")
MODEL = os.getenv("MODEL", "claude-3-5-sonnet")

client = OpenAI(api_key=PC_KEY, base_url=f"{HOST}/assistant/{ASSISTANT}")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_text}]
    )
    await update.message.reply_text(resp.choices[0].message.content)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

if __name__ == "__main__":
    print("Argos Telegram -> Pinecone 24/7 iniciado")
    app.run_polling()

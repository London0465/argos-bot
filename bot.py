import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

TOKEN = os.getenv("8506361405:AAENIpNpf7WQu-f971BuO1DCgcodvWAN_sE")
PC_KEY = os.getenv("pcsk_3HBzas_Gjf2rDY2ADBFCocedTxxEj1hgFL4UaGuCKHdCPyBKpJH5q7JAMc2E6c16im9rMp")
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

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Argos Telegram -> Pinecone 24/7 iniciado")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

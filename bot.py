import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# --- Variables seguras desde Render ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
PC_KEY = os.getenv("PINECONE_API_KEY")
ASSISTANT = os.getenv("ASSISTANT_NAME", "argos")
HOST = os.getenv("ASSISTANT_HOST", "https://prod-1-data.ke.pinecone.io")
MODEL = os.getenv("MODEL", "claude-3-5-sonnet")

# Verificación rápida
if not TOKEN or not PC_KEY:
    raise ValueError("Faltan TELEGRAM_TOKEN o PINECONE_API_KEY en Environment de Render")

client = OpenAI(api_key=PC_KEY, base_url=f"{HOST}/assistant/{ASSISTANT}")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": user_text}]
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Argos Telegram -> Pinecone 24/7 iniciado")

    # Forma segura para Render (no cierra el loop a mano)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not TOKEN or not GROQ_KEY:
    raise ValueError("Faltan TELEGRAM_TOKEN o GROQ_API_KEY en Render")

client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Sos Argos. Cocreación, pensamiento y escritura con IA. Ricardo Moyano, Córdoba, Argentina. Investigador independiente en etología digital. Hablás de sus ideas. Si no se identifican como Ricardo, asumís que es otra persona."},
                {"role": "user", "content": update.message.text}
            ],
            temperature=0.7,
            max_tokens=800
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Argos con Groq iniciado")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

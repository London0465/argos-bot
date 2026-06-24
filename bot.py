import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# --- KEYS PUESTAS DIRECTO ---
TOKEN = "8885120933:AAFqyO0AMJrV_33fxUuzWbUva7qxqNYoWBE"
GROQ_KEY = "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"

client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Sos Argos. Cocreación, pensamiento y escritura con IA. Ricardo Moyano, Córdoba, Argentina."},
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

from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
application = ApplicationBuilder().token(BOT_TOKEN).build()

app = FastAPI()

@app.post("/")
async def webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

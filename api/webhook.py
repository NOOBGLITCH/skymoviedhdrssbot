from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import logging
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Example command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Bot is live.")

dispatcher.add_handler(CommandHandler("start", start))

app = FastAPI()

@app.post("/")
async def process_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return {"ok": True}

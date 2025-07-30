from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os
import logging
from threading import Lock

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Read environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

# Global dispatcher
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=4, use_context=True)
dispatcher_lock = Lock()

# FastAPI app instance
app = FastAPI()

# Example command handler
def start(update, context):
    update.message.reply_text("Hello from your Vercel bot!")

# Register the handler
dispatcher.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.post("/webhook")
async def process_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)

    # Synchronize dispatcher access
    with dispatcher_lock:
        dispatcher.process_update(update)

    return {"ok": True}


# /api/webhook.py

import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_IDS = [int(cid) for cid in os.getenv("TELEGRAM_CHAT_ID").split(",")]
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None, use_context=True)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.process_update(update)
    return "ok", 200

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Bot is alive on Vercel.")

@app.route("/", methods=["GET"])
def home():
    return "Bot is live", 200

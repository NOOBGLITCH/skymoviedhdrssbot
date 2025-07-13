# telegram_bot.py
import telegram
from telegram.constants import ParseMode # Corrected import for ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(message):
    # Handle multiple chat IDs if provided as a comma-separated string
    chat_ids = [chat_id.strip() for chat_id in TELEGRAM_CHAT_ID.split(',')]

    for chat_id in chat_ids:
        try:
            bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN, # Corrected usage of ParseMode
                disable_web_page_preview=False
            )
            print(f"Telegram message sent successfully to chat ID: {chat_id}.")
        except telegram.error.TelegramError as e:
            print(f"Error sending Telegram message to chat ID {chat_id}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while sending Telegram message to chat ID {chat_id}: {e}")
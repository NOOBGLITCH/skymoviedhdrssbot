# telegram_bot.py
import telegram # pip install python-telegram-bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Initialize the bot outside the function to avoid re-initializing on every call
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(message):
    """
    Sends a message to the configured Telegram chat.
    """
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode=telegram.ParseMode.MARKDOWN, # Use Markdown for formatting
            disable_web_page_preview=False # Allow link previews
        )
        print("Telegram message sent successfully.")
    except telegram.error.TelegramError as e:
        print(f"Error sending Telegram message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while sending Telegram message: {e}")
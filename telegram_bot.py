# telegram_bot.py
import telegram
from telegram.constants import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

async def send_telegram_message(message):
    chat_ids = [chat_id.strip() for chat_id in TELEGRAM_CHAT_ID.split(',')]

    for chat_id in chat_ids:
        try:
            await bot.send_message( # Added 'await' here
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False
            )
            print(f"Telegram message sent successfully to chat ID: {chat_id}.")
        except telegram.error.TelegramError as e:
            print(f"Error sending Telegram message to chat ID {chat_id}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while sending Telegram message to chat ID {chat_id}: {e}")

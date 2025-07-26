import time
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import WEBSITE_URL, LAST_SEEN_FILE, CHECK_INTERVAL_MINUTES, LAST_KNOWN_URL_FILE
from scraper import get_current_website_data
from storage import load_last_seen_data, save_last_seen_data
from telegram_bot import send_telegram_message
from url_resolver import resolve_movie_website_url
from datetime import datetime
import pytz

last_notification_timestamp = 0

def get_current_ist_timestamp():
    ist_timezone = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist_timezone)
    return now_ist.strftime('%Y-%m-%d %H:%M:%S IST')

async def monitor_website_changes():
    global last_notification_timestamp

    current_monitoring_url = await resolve_movie_website_url()

    if not current_monitoring_url:
        print(f"[{get_current_ist_timestamp()}] No active website URL found. Skipping movie check.")
        return

    print(f"[{get_current_ist_timestamp()}] Checking for new movies on {current_monitoring_url}...")
    
    last_seen_fingerprints = load_last_seen_data(LAST_SEEN_FILE)
    current_fingerprints, current_movie_details = get_current_website_data(current_monitoring_url)

    if not current_fingerprints:
        print("Could not retrieve current movie data from the active URL. Skipping update.")
        return

    new_movie_fingerprints = current_fingerprints - last_seen_fingerprints

    new_movies_for_notification = [
        movie_detail for movie_detail in current_movie_details
        if movie_detail['fingerprint'] in new_movie_fingerprints
    ]

    new_posts_count = len(new_movies_for_notification)

    if new_posts_count > 0:
        current_time = time.time()
        
        if (current_time - last_notification_timestamp) < (CHECK_INTERVAL_MINUTES * 60):
            print(f"[{get_current_ist_timestamp()}] New movies found, but notification cooldown is active. Skipping notification.")
            save_last_seen_data(current_fingerprints, LAST_SEEN_FILE)
            return

        movie_entries = [f"🎬 **{movie.get('name', 'Unknown Movie')}**" for movie in new_movies_for_notification]

        notification_message = " **🎬 New Movie Added! ✅** \n\n" + "\n\n".join(movie_entries)
        
        # Add the requested line at the end
        notification_message += "\n\nCheck always update on https://www.skybap.com"
        
        await send_telegram_message(notification_message)
        
        last_notification_timestamp = current_time
        save_last_seen_data(current_fingerprints, LAST_SEEN_FILE)
        print(f"Detected and notified about {new_posts_count} new movie(s).")
    else:
        print("Detected changes in fingerprints, but no new posts to report.")
        save_last_seen_data(current_fingerprints, LAST_SEEN_FILE)

async def start_monitoring_bot():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(monitor_website_changes, 'interval', minutes=CHECK_INTERVAL_MINUTES)
    
    scheduler.start()
    
    await monitor_website_changes()

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(start_monitoring_bot())
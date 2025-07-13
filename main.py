# main.py
import time
import schedule 
from config import WEBSITE_URL, LAST_SEEN_FILE, CHECK_INTERVAL_MINUTES, LAST_KNOWN_URL_FILE
from scraper import get_current_website_data
from storage import load_last_seen_data, save_last_seen_data
from telegram_bot import send_telegram_message
from utils import get_current_ist_timestamp
from url_resolver import resolve_movie_website_url

last_notification_timestamp = 0

def monitor_website_changes():
    global last_notification_timestamp

    current_monitoring_url = resolve_movie_website_url()

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

    if new_movie_fingerprints:
        current_time = time.time()
        
        # Check if cooldown is active
        if (current_time - last_notification_timestamp) < (CHECK_INTERVAL_MINUTES * 60):
            print(f"[{get_current_ist_timestamp()}] New movies found, but notification cooldown is active. Skipping notification.")
            save_last_seen_data(current_fingerprints, LAST_SEEN_FILE) # Update to avoid re-notifying later
            return

        notification_message = "📢 **Website Update Detected!** 📢\n\n"
        new_posts_count = 0
        
        for movie_detail in current_movie_details:
            if movie_detail['fingerprint'] in new_movie_fingerprints:
                new_posts_count += 1
                movie_name = movie_detail.get('name', 'Unknown Movie')
                movie_link = movie_detail.get('link', current_monitoring_url)
                timestamp = get_current_ist_timestamp()
                
                notification_message += f"🎬 **{movie_name}**\n"
                notification_message += f"🔗 [Link]({movie_link})\n"
                notification_message += f"⏰ {timestamp}\n\n"

        if new_posts_count > 0:
            notification_message += f"\nCheck out all the latest updates here: {current_monitoring_url}"
            send_telegram_message(notification_message)
            
            last_notification_timestamp = current_time # Update cooldown timestamp
            save_last_seen_data(current_fingerprints, LAST_SEEN_FILE)
            print(f"Detected and notified about {new_posts_count} new movie(s).")
        else:
            print("Detected changes in fingerprints, but no new posts to report.")
            save_last_seen_data(current_fingerprints, LAST_SEEN_FILE)

    else:
        print("No new movies detected.")

def start_monitoring_bot():
    print(f"Bot starting. Monitoring every {CHECK_INTERVAL_MINUTES} minutes.")
    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(monitor_website_changes)

    monitor_website_changes() 

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_monitoring_bot()
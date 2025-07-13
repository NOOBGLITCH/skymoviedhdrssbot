# url_resolver.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from telegram_bot import send_telegram_message # Import for sending notifications
from storage import load_last_known_url, save_last_known_url # Import for URL persistence
from config import WEBSITE_URL, SKYBAP_URL, LAST_KNOWN_URL_FILE # Import config

def resolve_movie_website_url():
    """
    Determines the current active URL for the movie website.
    It first tries the primary URL. If that fails, it attempts to
    find a new URL from the fallback (skybap.com).
    Sends Telegram notifications if the URL changes or becomes unreachable.

    Returns:
        str: The currently active website URL, or None if no URL could be found.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    last_known_active_url = load_last_known_url(LAST_KNOWN_URL_FILE)
    effective_url = None

    print(f"Attempting to reach primary URL: {WEBSITE_URL}")
    try:
        # Try the primary URL first
        response = requests.get(WEBSITE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        effective_url = WEBSITE_URL
        print("Primary URL is reachable.")

    except requests.exceptions.RequestException as e:
        print(f"Primary URL {WEBSITE_URL} is unreachable: {e}. Trying fallback URL {SKYBAP_URL}...")
        
        try:
            # If primary fails, try the fallback URL to find a new main URL
            fallback_response = requests.get(SKYBAP_URL, headers=headers, timeout=15)
            fallback_response.raise_for_status()
            fallback_soup = BeautifulSoup(fallback_response.text, 'html.parser')
            
            # Find the span with the specific style and text
            # The structure for skymovieshd.land on skybap.com might change.
            # We are looking for <span style="color: red">SkymoviesHD.Land</span>
            # and assuming its parent <a> tag contains the href.
            span_tag = fallback_soup.find('span', string='SkymoviesHD.Land', style="color: red")
            
            if span_tag:
                link_tag = span_tag.find_parent('a') # Get the parent <a> tag
                if link_tag and link_tag.has_attr('href'):
                    # The href might be relative, so use urljoin to make it absolute if necessary
                    new_url = urljoin(SKYBAP_URL, link_tag['href'])
                    # Basic validation: ensure it looks like a valid URL
                    if new_url.startswith('http'): 
                        effective_url = new_url
                        print(f"Found new URL from fallback: {effective_url}")
                    else:
                        print(f"Found href '{link_tag['href']}' but it's not a valid URL. Skipping.")
                else:
                    print("Could not find a valid link (parent <a>) for 'SkymoviesHD.Land' span on fallback page.")
            else:
                print("Could not find 'SkymoviesHD.Land' span on fallback page.")

        except requests.exceptions.RequestException as e:
            print(f"Fallback URL {SKYBAP_URL} also unreachable or failed: {e}")
            effective_url = None # Indicate total failure to resolve

    # --- Notification and Persistence Logic ---
    if effective_url and effective_url != last_known_active_url:
        message = f"🚨 **Monitoring URL Changed!** 🚨\n"
        if last_known_active_url:
            message += f"Old URL: {last_known_active_url}\n"
        message += f"New active URL for SkymoviesHD: {effective_url}\n"
        send_telegram_message(message)
        save_last_known_url(effective_url, LAST_KNOWN_URL_FILE)
    elif not effective_url and last_known_active_url:
        # If we had a last known URL but now can't find any
        message = f"⚠️ **Monitoring URL Lost!** ⚠️\n"
        message += f"Could not reach primary ({WEBSITE_URL}) or find new URL from fallback ({SKYBAP_URL}).\n"
        message += f"Last known URL was: {last_known_active_url}\n"
        message += "Monitoring paused until a valid URL is found."
        send_telegram_message(message)
        # We don't save None, so last_known_url persists until a new one is found

    return effective_url
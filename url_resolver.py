# url_resolver.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from telegram_bot import send_telegram_message
from storage import load_last_known_url, save_last_known_url
from config import WEBSITE_URL, SKYBAP_URL, LAST_KNOWN_URL_FILE

async def resolve_movie_website_url(): # Made async
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    last_known_active_url = load_last_known_url(LAST_KNOWN_URL_FILE)
    effective_url = None

    print(f"Attempting to reach primary URL: {WEBSITE_URL}")
    try:
        response = requests.get(WEBSITE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        effective_url = WEBSITE_URL
        print("Primary URL is reachable.")

    except requests.exceptions.RequestException as e:
        print(f"Primary URL {WEBSITE_URL} is unreachable: {e}. Trying fallback URL {SKYBAP_URL}...")
        
        try:
            fallback_response = requests.get(SKYBAP_URL, headers=headers, timeout=15)
            fallback_response.raise_for_status()
            fallback_soup = BeautifulSoup(fallback_response.text, 'html.parser')
            
            span_tag = fallback_soup.find('span', string='SkymoviesHD.Land', style="color: red")
            
            if span_tag:
                link_tag = span_tag.find_parent('a')
                if link_tag and link_tag.has_attr('href'):
                    new_url = urljoin(SKYBAP_URL, link_tag['href'])
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
            effective_url = None

    if effective_url and effective_url != last_known_active_url:
        message = f"🚨 **Monitoring URL Changed!** 🚨\n"
        if last_known_active_url:
            message += f"Old URL: {last_known_active_url}\n"
        message += f"New active URL for SkymoviesHD: {effective_url}\n"
        await send_telegram_message(message) # Added 'await' here
        save_last_known_url(effective_url, LAST_KNOWN_URL_FILE)
    elif not effective_url and last_known_active_url:
        message = f"⚠️ **Monitoring URL Lost!** ⚠️\n"
        message += f"Could not reach primary ({WEBSITE_URL}) or find new URL from fallback ({SKYBAP_URL}).\n"
        message += f"Last known URL was: {last_known_active_url}\n"
        message += "Monitoring paused until a valid URL is found."
        await send_telegram_message(message) # Added 'await' here

    return effective_url

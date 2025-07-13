# scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import CSS_POST_SELECTOR # Only import CSS selector from config
from utils import get_element_fingerprint

# get_current_website_data now accepts website_url as an argument
def get_current_website_data(website_url):
    """
    Fetches the website content from the given website_url, parses it,
    and extracts movie details.
    Returns a tuple: (set of fingerprints, list of movie details for notification).
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(website_url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <a> tags matching the selector
        movie_elements = soup.select(CSS_POST_SELECTOR)
        
        current_fingerprints = set()
        movie_details_for_notification = []

        for element in movie_elements:
            # Get the full URL for the fingerprint
            fingerprint = get_element_fingerprint(element, website_url)
            if not fingerprint:
                continue # Skip if no href found

            current_fingerprints.add(fingerprint)

            # Extract movie name: text content of <a>, but remove the <img> tag first
            # Create a copy to modify without affecting the original soup structure if needed elsewhere
            element_copy = BeautifulSoup(str(element), 'html.parser')
            img_tag = element_copy.find('img')
            if img_tag:
                img_tag.extract() # Remove the image tag

            movie_name = element_copy.get_text(strip=True)
            
            movie_details_for_notification.append({
                'name': movie_name,
                'link': fingerprint, # fingerprint is already the full URL
                'fingerprint': fingerprint
            })
            
        return current_fingerprints, movie_details_for_notification

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {website_url}: {e}")
        return set(), []
    except Exception as e:
        print(f"Error parsing content or other issue in scraper: {e}")
        return set(), []
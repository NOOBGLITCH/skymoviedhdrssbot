import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import CSS_POST_SELECTOR

# Removed: from utils import get_element_fingerprint

def get_current_website_data(website_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(website_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        movie_elements = soup.select(CSS_POST_SELECTOR)
        
        current_fingerprints = set()
        movie_details_for_notification = []

        for element in movie_elements:
            href = element.get('href')
            if href:
                # get_element_fingerprint logic is inlined here
                fingerprint = urljoin(website_url, href)
            else:
                continue

            current_fingerprints.add(fingerprint)

            element_copy = BeautifulSoup(str(element), 'html.parser')
            img_tag = element_copy.find('img')
            if img_tag:
                img_tag.extract()

            movie_name = element_copy.get_text(strip=True)
            
            movie_details_for_notification.append({
                'name': movie_name,
                'link': fingerprint,
                'fingerprint': fingerprint
            })
            
        return current_fingerprints, movie_details_for_notification

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {website_url}: {e}")
        return set(), []
    except Exception as e:
        print(f"Error parsing content or other issue in scraper: {e}")
        return set(), []
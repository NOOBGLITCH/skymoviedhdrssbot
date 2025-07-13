# utils.py
import hashlib
from datetime import datetime
import pytz
from urllib.parse import urljoin

def get_element_fingerprint(element, base_url):
    href = element.get('href')
    if href:
        full_url = urljoin(base_url, href)
        return full_url
    return None

def get_current_ist_timestamp():
    ist_timezone = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist_timezone)
    return now_ist.strftime('%Y-%m-%d %H:%M:%S IST')
# storage.py
import json

def load_last_seen_data(filename):
    """
    Loads the set of last seen movie fingerprints from a JSON file.
    Returns an empty set if the file doesn't exist or is invalid.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_last_seen_data(data, filename):
    """
    Saves the current set of movie fingerprints to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(list(data), f, ensure_ascii=False, indent=2)

def load_last_known_url(filename):
    """
    Loads the last known active monitoring URL from a text file.
    Returns None if the file doesn't exist.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_known_url(url, filename):
    """
    Saves the given URL as the last known active monitoring URL to a text file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(url)
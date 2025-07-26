import json

def load_last_seen_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_last_seen_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(list(data), f, ensure_ascii=False, indent=2)

def load_last_known_url(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_known_url(url, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(url)
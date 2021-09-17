from datetime import datetime
from typing import Dict
import warnings

from config import MAX_LEN


def beautify(string):
    return string.replace('_', ' ').replace('-', ' ').title()


def unbeautify(string):
    return string.replace(' ', '-').lower()


def generate_short_title(title):
    short_title = title or 'Untitled'
    if len(title) >= MAX_LEN:
        short_title = title[:MAX_LEN - len(' ... ')] + ' ... '
    short_title = short_title.replace('$', '')
    return short_title


def get_week(d=datetime.today()):
    return (int(d.strftime("%W")) + 52 - 5) % 52


def merge_dictionaries(main: Dict, fallback: Dict):
    merged = main
    for key in fallback.keys():
        if key not in main.keys():
            merged[key] = fallback[key]
        elif type(fallback[key]) == dict:
            if not type(merged[key]) == dict:
                warnings.warn(
                    f"Main dictionary has invalid format. Replacing entry with key {key} with fallback value.")
                merged[key] = fallback[key]
            merged[key] = merge_dictionaries(merged[key], fallback[key])
    return merged

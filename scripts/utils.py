import re
from datetime import datetime
from typing import Dict
import warnings

from config import MAX_LEN


def beautify(string):
    return string.replace('_', ' ').replace('-', ' ').title()


def unbeautify(string):
    return string.replace(' ', '-').lower()


def normalize(string):
    return string.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')


def generate_short_title(title):
    short_title = title or 'Untitled'
    if len(title) >= MAX_LEN:
        short_title = title[:MAX_LEN - len(' ... ')] + ' ... '
    short_title = short_title.replace('$', '')
    return short_title


def get_week(d=datetime.today()):
    return (int(d.strftime("%W")) + 52 - 5) % 52


def parse_zoom_link(browser_join_link: str):
    match = re.search(r'(?:/j/|&confno=)(?P<confno>\d*)(?:&zc=0)?(?:\?|&)pwd=(?P<pwd>.*?)(?:#success|$)', browser_join_link)
    if not match:
        return None
    else:
        return match.groupdict()['confno'], match.groupdict()['pwd']


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

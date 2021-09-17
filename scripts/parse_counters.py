#!/usr/bin/python3
import re
from pathlib import Path
from typing import Dict
from config import DEFAULT_IMPORT_INDENTATION


def parse_counters(filepath: Path, break_point: Dict) -> Dict:
    if not filepath.is_file():
        return {}
    counters: Dict = {}
    with open(filepath) as f:
        for line in f:
            counter, _, num = re.search(r"(.*): (\d*\.)*?(\d*)", line).groups()
            num = int(num)
            if counter in break_point and num >= break_point[counter]:
                return counters
            counters[counter] = num
    return counters


def dict2setcounters(counters: Dict):
    counters_as_list = [(counter, counters[counter]) for counter in counters.keys()]
    return ''.join(' ' * DEFAULT_IMPORT_INDENTATION + r'\setcounter{' + counter + '}{' + str(num) + '}\n'
                   for (counter, num) in counters_as_list)

#!/usr/bin/python3
from courses import Courses
import sys


def open_spec(specification: str):
    current = Courses().current

    switcher = {
        'full': current.notes.open_full,
        'master': current.notes.open_master
    }

    if specification in switcher.keys():
        return switcher[specification]()

    link_type = {
        'webpage': 'webpage',
        'w': 'webpage',
        'url': 'webpage',
        'u': 'webpage',
        'ecampus': 'ecampus',
        'e': 'ecampus',
        'sciebo': 'sciebo',
        's': 'sciebo',
        'basis': 'basis',
        'b': 'basis',
        'github': 'github',
        'g': 'github'
    }
    return current.links.open(link_type[specification])


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        open_spec(arg)

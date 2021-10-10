#!/usr/bin/python3
from courses import Courses
from exercises import Exercises
from rofi import rofi
from config import MAX_LEN
import sys


def rofi_pick_exercise(spec: str = 'writeup'):
    exercises = Courses().current.exercises
    switcher = {
        'writeup': Exercises.writeups,
        'solution': Exercises.solutions,
        'sheet': Exercises.sheets
    }

    sorted_ex = sorted(switcher[spec].fget(exercises), key=lambda e: -e.number)

    options = [
        "{number: >2}".format(
            number=ex.number
        )
        for ex in sorted_ex
    ]

    switcher = {
        'writeup': 'writeup',
        'solution': 'solution',
        'sheet': 'sheet'
    }

    key, index, selected = rofi('Select number of exercise {spec}'.format(spec=switcher[spec]), options, [
        '-lines', max(5, min(15, len(sorted_ex))),
        '-markup-rows',
        '-kb-custom-1', 'Alt+n'
    ])

    if key == 0:
        sorted_ex[index].open()
    elif key == 1:
        pass  # TODO: make new exercise


if __name__ == '__main__':
    if not len(sys.argv) == 1:
        print('Please specify exactly one of "writeup", "solution" and "sheet"')
        exit(1)
    rofi_pick_exercise('sheet')
    exit(0)

#!/usr/bin/python3

import locale
import re
import subprocess
from datetime import datetime

from config import get_week, DATE_FORMAT, LOCALE, DEFAULT_MASTER_FILE_NAME

# TODO
locale.setlocale(locale.LC_TIME, LOCALE)


def number2filename(n):
    return 'lec_{0:02d}.tex'.format(n)


def filename2number(s):
    return int(str(s).replace('.tex', '').replace('lec_', ''))


class Lecture:
    def __init__(self, file_path, course):
        with file_path.open() as f:
            for line in f:
                lecture_match = re.search(r'lecture{(.*?)}{(.*?)}{(.*)}', line)
                if lecture_match:
                    break

        # number = int(lecture_match.group(1))

        date_str = lecture_match.group(2)
        date = datetime.strptime(date_str, DATE_FORMAT)
        week = get_week(date)

        title = lecture_match.group(3)

        self.file_path = file_path
        self.date = date
        self.week = week
        self.number = filename2number(file_path.stem)
        self.title = title
        self.course = course

    def edit(self):
        subprocess.Popen([
            "x-terminal-emulator",
            "-e", "zsh", "-i", "-c",
            f"\\vim --servername kulak --remote-silent {str(self.file_path)}"
        ])

    def __str__(self):
        return f'<Lecture {self.course.info["short"]} {self.number} "{self.title}">'


class Lectures(list):
    def __init__(self, script):
        self.course = script.course
        self.script = script
        if 'lectures' in script.info:
            self.info = script.info['lectures']
        else:
            self.info = []
        if 'path' in self.info:
            self.root = script.root / self.info['path']
            self.root.mkdir(parents=True, exist_ok=True)
        else:
            self.root = script.root
        list.__init__(self, self.read_files())

    def read_files(self):
        files = self.root.glob('lec_*.tex')
        return sorted((Lecture(f, self.course) for f in files), key=lambda l: l.number)

    def parse_lecture_spec(self, string):
        if len(self) == 0:
            return 0

        if string.isdigit():
            return int(string)
        elif string == 'last':
            return self[-1].number
        elif string == 'prev':
            return self[-1].number - 1

    def parse_range_string(self, arg):
        all_numbers = [lecture.number for lecture in self]
        if 'all' in arg:
            return all_numbers

        if '-' in arg:
            start, end = [self.parse_lecture_spec(bit) for bit in arg.split('-')]
            return list(set(all_numbers) & set(range(start, end + 1)))

        return [self.parse_lecture_spec(arg)]

    def new_lecture(self):
        if len(self) != 0:
            new_lecture_number = self[-1].number + 1
        else:
            new_lecture_number = 1

        new_lecture_path = self.root / number2filename(new_lecture_number)

        today = datetime.today()
        date = today.strftime(DATE_FORMAT)

        new_lecture_path.touch()
        new_lecture_path.write_text(f'\\lecture{{{new_lecture_number}}}{{{date}}}{{}}\n')

        self.read_files()

        lec = Lecture(new_lecture_path, self.course)

        return lec


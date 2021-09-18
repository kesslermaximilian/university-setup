#!/usr/bin/python3
import locale
import os
import re
import warnings
from datetime import datetime

from config import DATE_FORMAT, LOCALE, DEFAULT_NEW_LECTURE_HEADER, DEFAULT_LECTURE_SEARCH_REGEX, \
    DEFAULT_NEW_LECTURE_TITLE
from edit import edit
from utils import get_week

# TODO
locale.setlocale(locale.LC_TIME, LOCALE)


def number2filename(n):
    return 'lec_{0:02d}.tex'.format(n)


def filename2number(s):
    return int(str(s).replace('.tex', '').replace('lec_', ''))


class Lecture:
    def __init__(self, file_path, notes):
        with file_path.open() as f:
            for line in f:
                lecture_match = re.search(DEFAULT_LECTURE_SEARCH_REGEX, line)
                if lecture_match:
                    break

        if lecture_match:
            date_str = lecture_match.group(2)
            try:
                date = datetime.strptime(date_str, DATE_FORMAT)
            except ValueError:
                warnings.warn(f"Invalid date format found in lecture file {file_path}. Specify time in format"
                              f"'{DATE_FORMAT}' that you set in the config.py file.")
                date = datetime.min
            week = get_week(date)

            title = lecture_match.group(3)
        else:
            date = datetime.min
            week = get_week(date)

            title = 'Error while parsing lecture file'

        self.file_path = file_path
        self.date = date
        self.week = week
        self.number = filename2number(file_path.stem)
        self.title = title
        self.notes = notes

    def edit(self):
        edit(self.file_path, rootpath=self.notes.root, env=self.notes.environment())

    def __str__(self):
        return f'<Lecture {self.course.info["short"]} {self.number} "{self.title}">'


class Lectures(list):
    def __init__(self, notes):
        self.course = notes.course
        self.notes = notes
        if 'lectures' in notes.info:
            self.info = notes.info['lectures']
        else:
            self.info = []
        if 'path' in self.info:
            self.root = notes.root / self.info['path']
            self.root.mkdir(parents=True, exist_ok=True)
        else:
            self.root = notes.root
        list.__init__(self, self.read_files())

    def read_files(self):
        files = self.root.glob('lec_*.tex')
        return sorted((Lecture(f, self.notes) for f in files), key=lambda l: l.number)

    def parse_lecture_spec(self, string):
        if len(self) == 0:
            return 0

        if string.isdigit():
            return int(string)
        elif string == 'last':
            return self[-1].number
        elif string == 'prev':
            return self[-1].number - 1

    def parse_range_string_section(self, arg):
        if 'all' in arg:
            return [lecture.number for lecture in self]

        if '-' in arg:
            start, end = [self.parse_lecture_spec(bit) for bit in arg.split('-')]
            return list(range(start, end + 1))

        return [self.parse_lecture_spec(arg)]

    def parse_range_string(self, arg):
        all_numbers = [lecture.number for lecture in self]
        sets = [set(self.parse_range_string_section(part)) for part in arg.split(',')]
        return list(set.union(*sets) & set(all_numbers))

    def new_lecture(self):
        if len(self) != 0:
            new_lecture_number = self[-1].number + 1
        else:
            new_lecture_number = 1

        new_lecture_path = self.root / number2filename(new_lecture_number)

        today = datetime.today()
        date = today.strftime(DATE_FORMAT)

        vimtex_root_str = f"%! TEX root = {str(os.path.relpath(self.notes.master_file, self.root))}\n"
        header_str = DEFAULT_NEW_LECTURE_HEADER.format(
            number=new_lecture_number, date=date, title=DEFAULT_NEW_LECTURE_TITLE)
        new_lecture_path.touch()
        new_lecture_path.write_text(vimtex_root_str + header_str)

        self.read_files()

        lec = Lecture(new_lecture_path, self.notes)

        return lec

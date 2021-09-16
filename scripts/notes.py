#!/usr/bin/python3
from pathlib import Path
import subprocess

from lectures import Lectures, number2filename
from config import *


class Notes:
    def __init__(self, course):
        self.course = course
        if 'notes' in course.info:
            self.info = course.info['notes']
        else:
            self.info = []
        if 'path' in self.info:
            self.root = course.path / self.info['path']
        else:
            self.root = course.path
        if 'master_file' in self.info:
            self.master_file = self.root / self.info['master_file']
        else:
            self.master_file = self.root / DEFAULT_MASTER_FILE_NAME
        self._lectures = None

    @staticmethod
    def get_header_footer(filepath):
        part = 0
        header = ''
        footer = ''
        with filepath.open() as f:
            for line in f:
                # order of if-statements is important here!
                if 'end lectures' in line:
                    part = 2

                if part == 0:
                    header += line
                if part == 2:
                    footer += line

                if 'start lectures' in line:
                    part = 1
        return header, footer

    def new_lecture(self):
        lec = self.lectures.new_lecture()
        if lec.number == 1:
            self.update_lectures_in_master([1])
        else:
            self.update_lectures_in_master([lec.number - 1, lec.number])
        return lec

    def update_lectures_in_master(self, r):
        header, footer = self.get_header_footer(self.master_file)
        body = ''.join(
            ' ' * 4 + r'\input{' + number2filename(number) + '}\n' for number in r)
        self.master_file.write_text(header + body + footer)

    def compile_master(self):
        result = subprocess.run(
            ['latexmk', '-f', '-interaction=nonstopmode', str(self.master_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(self.root)
        )
        return result.returncode

    @property
    def lectures(self):
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

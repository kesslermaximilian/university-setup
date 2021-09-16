#!/usr/bin/python3
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
            self.root.mkdir(parents=True, exist_ok=True)
        else:
            self.root = course.path
        if 'master_file' in self.info:
            self.master_file = self.root / self.info['master_file']
        else:
            self.master_file = self.root / DEFAULT_MASTER_FILE_NAME
        if 'full_file' in self.info:
            self.full_file = self.root / self.info['full_file']
        else:
            self.full_file = None
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
        self.update_lectures_in_full(self.lectures.parse_range_string('all'))
        return lec

    def update_lectures_in_file(self, filename, lecture_list):
        header, footer = self.get_header_footer(filename)
        if self.lectures.root.relative_to(self.root) == Path('.'):
            input_command = r'\input{'
        else:
            input_command = r'\import{' + str(self.lectures.root.relative_to(self.root)) + '/}{'
        body = ''.join(
            ' ' * 4 + input_command + number2filename(number) + '}\n' for number in lecture_list)
        filename.write_text(header + body + footer)

    def update_lectures_in_master(self, lecture_list):
        self.update_lectures_in_file(self.master_file, lecture_list)

    def update_lectures_in_full(self, lecture_list):
        if self.full_file:
            self.update_lectures_in_file(self.full_file, lecture_list)

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

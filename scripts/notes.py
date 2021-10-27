#!/usr/bin/python3
import os
import subprocess
from pathlib import Path
from typing import Dict

from config import LECTURE_START_MARKER, LECTURE_END_MARKER, DEFAULT_IMPORT_INDENTATION, \
    DEFAULT_LATEX_COUNTER_AUX_FILE_EXTENSION
from window_subprocess import edit
from lectures import Lectures, number2filename
from parse_counters import parse_counters, dict2setcounters


class Notes:
    def __init__(self, course):
        self.course = course  # A course
        self.info: Dict = course.info['notes']
        self.root: Path = course.path / self.info['path']
        self.root.mkdir(parents=True, exist_ok=True)
        self.master_file: Path = self.root / self.info['master_file']
        self.full_file: Path = self.root / self.info['full_file']
        self.texinputs: Path = self.root / self.info['texinputs']
        self._lectures = None

    @staticmethod
    def get_header_footer(filepath):
        part = 0
        header = ''
        footer = ''
        with filepath.open() as f:
            for line in f:
                # order of if-statements is important here!
                if LECTURE_END_MARKER in line:
                    part = 2

                if part == 0:
                    header += line
                if part == 2:
                    footer += line

                if LECTURE_START_MARKER in line:
                    part = 1
        return header, footer

    def new_lecture(self):
        lec = self.lectures.new_lecture()
        if lec.number == 1:
            self.update_lectures_in_master([1])
        else:
            self.update_lectures_in_master([lec.number - 1, lec.number])
        self._lectures = None  # This causes the lectures to be re-computed
        self.update_lectures_in_full(self.lectures.parse_range_string('all'))
        return lec

    def input_lecture_command(self, num: int):
        if self.lectures.root.relative_to(self.root) == Path('.'):
            input_command = r'\input{'
        else:
            input_command = r'\import{' + str(self.lectures.root.relative_to(self.root)) + '/}{'
        return ' ' * DEFAULT_IMPORT_INDENTATION + input_command + number2filename(num) + '}\n'

    def set_counters(self, lecture_list, lec, setcounters=False):
        if not setcounters:
            return ''
        if lec - 1 not in lecture_list and self.full_file:
            return dict2setcounters(parse_counters(
                self.full_file.with_suffix(DEFAULT_LATEX_COUNTER_AUX_FILE_EXTENSION),
                {'lecture': lec}
            ))
        return ''

    def update_lectures_in_file(self, filename, lecture_list, setcounters=False):
        header, footer = self.get_header_footer(filename)
        body = ''.join([self.set_counters(lecture_list, num, setcounters) + self.input_lecture_command(num)
                        for num in lecture_list])
        filename.write_text(header + body + footer)

    def update_lectures_in_master(self, lecture_list):
        self.update_lectures_in_file(self.master_file, lecture_list, True)

    def update_lectures_in_full(self, lecture_list):
        if self.full_file:
            self.update_lectures_in_file(self.full_file, lecture_list)

    def edit_master(self):
        edit(self.master_file, rootpath=self.root, env=self.environment())

    def edit_full(self):
        edit(self.full_file, rootpath=self.root, env=self.environment())

    def open_master(self):
        result = subprocess.run(
            ['zathura', str(self.master_file.with_suffix('.pdf'))],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode

    def open_full(self):
        result = subprocess.run(
            ['zathura', str(self.full_file.with_suffix('.pdf'))],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode

    def open_terminal(self):
        result = subprocess.Popen(
            ['termite'], env=self.environment(), cwd=self.root
        )

    def compile_master(self):
        result = subprocess.run(
            ['latexmk', '-f', '-interaction=nonstopmode', '-dvi-', '-pdf', str(self.master_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(self.root),
            env=self.environment()
        )
        return result.returncode

    def compile_full(self):
        if not self.full_file:
            return 0
        result = subprocess.run(
            ['latexmk', '-f', '-interaction=nonstopmode', '-dvi-', '-pdf', str(self.full_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(self.root),
            env=self.environment()
        )
        return result.returncode

    def environment(self):
        env = os.environ
        env["TEXINPUTS"] = str(self.texinputs) + '//:'
        return env

    @property
    def lectures(self):
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

#!/usr/bin/python3
from pathlib import Path
import yaml

from lectures import Lectures
from script import Script
from config import ROOT, CURRENT_COURSE_ROOT, CURRENT_COURSE_SYMLINK, CURRENT_COURSE_WATCH_FILE, COURSE_IGNORE_FILE, \
    COURSE_INFO_FILE


class Course:
    def __init__(self, path):
        self.path = path
        self.name = path.stem

        self.info = yaml.safe_load((path / COURSE_INFO_FILE).open())
        self._script = None

    @property
    def script(self):
        if not self._script:
            self._script = Script(self)
        return self._script

    def __eq__(self, other):
        if other is None:
            return False
        return self.path == other.path


def ignored_courses():
    with open(ROOT / COURSE_IGNORE_FILE) as ignore:
        lines = ignore.readlines()
        paths = []
        for line in lines:
            paths.append(ROOT / line.strip())
        return paths


def read_files():
    course_directories = [x for x in ROOT.iterdir() if x.is_dir() and x not in ignored_courses()]
    _courses = [Course(path) for path in course_directories]
    return sorted(_courses, key=lambda c: c.name)


class Courses(list):
    def __init__(self):
        list.__init__(self, read_files())

    @property
    def current(self):
        return Course(CURRENT_COURSE_ROOT.resolve())

    @current.setter
    def current(self, course):
        CURRENT_COURSE_SYMLINK.unlink()
        CURRENT_COURSE_SYMLINK.symlink_to(course.path)
        CURRENT_COURSE_WATCH_FILE.write_text('{}\n'.format(course.info['short']))

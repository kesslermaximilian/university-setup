#!/usr/bin/python3
from pathlib import Path
import yaml
import warnings

from lectures import Lectures
from notes import Notes
from config import ROOT, CURRENT_COURSE_ROOT, CURRENT_COURSE_SYMLINK, CURRENT_COURSE_WATCH_FILE, COURSE_IGNORE_FILE, \
    COURSE_INFO_FILE


class Course:
    def __init__(self, path):
        self.path = path
        self.name = path.stem
        if (path / COURSE_INFO_FILE).is_file():
            self.info = yaml.safe_load((path / COURSE_INFO_FILE).open())
        else:
            warnings.warn(f"No course info file found in directory '{path.stem}'. Place a {COURSE_INFO_FILE} "
                          f"file in the directory or add the directory to the course ignore file named"
                          f" '{COURSE_IGNORE_FILE}' in your root directory ({ROOT})")
            self.info = {'title': path.stem, 'short': path.stem}
        self._notes = None

    @property
    def notes(self):
        if not self._notes:
            self._notes = Notes(self)
        return self._notes

    def __eq__(self, other):
        if other is None:
            return False
        return self.path == other.path


def ignored_courses():
    if (ROOT / COURSE_IGNORE_FILE).is_file():
        with open(ROOT / COURSE_IGNORE_FILE) as ignore:
            lines = ignore.readlines()
            paths = []
            for line in lines:
                paths.append(ROOT / line.strip())
            return paths
    return []


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

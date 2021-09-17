#!/usr/bin/python3
import warnings

import yaml
from typing import List

from config import ROOT, CURRENT_COURSE_ROOT, CURRENT_COURSE_SYMLINK, CURRENT_COURSE_WATCH_FILE, COURSE_IGNORE_FILE, \
    COURSE_INFO_FILE_NAME, FALLBACK_COURSE_INFO_FILE
from notes import Notes
from links import Links
from utils import merge_dictionaries


class Course:
    def __init__(self, path):
        self.path = path
        self.name = path.stem
        if (path / COURSE_INFO_FILE_NAME).is_file():
            self.info = yaml.safe_load((path / COURSE_INFO_FILE_NAME).open())
        else:
            warnings.warn(f"No course info file found in directory '{path.stem}'. Place a {COURSE_INFO_FILE_NAME} "
                          f"file in the directory or add the directory to the course ignore file named"
                          f" '{COURSE_IGNORE_FILE}' in your root directory ({ROOT})")
            self.info = {'title': str(path.stem) + ' (unnamed course)'}
        if FALLBACK_COURSE_INFO_FILE.is_file():
            fallback_file = yaml.safe_load(FALLBACK_COURSE_INFO_FILE.open())
        else:
            warnings.warn(f"No fallback course info file found. Program might crash if your provided info files do not"
                          f"have the correct file format or are missing specified values. Provide the fallback course"
                          f"file at {FALLBACK_COURSE_INFO_FILE}.")
            fallback_file = {}
        self.info = merge_dictionaries(self.info, fallback_file)
        self._notes = None
        self._links = None

    @property
    def links(self) -> Links:
        if not self._links:
            self._links = Links(self)
        return self._links

    @property
    def notes(self) -> Notes:
        if not self._notes:
            self._notes = Notes(self)
        return self._notes

    def __eq__(self, other):
        if other is None:
            return False
        return self.path == other.path


def ignored_courses() -> List[Course]:
    if (ROOT / COURSE_IGNORE_FILE).is_file():
        with open(ROOT / COURSE_IGNORE_FILE) as ignore:
            lines = ignore.readlines()
            paths = []
            for line in lines:
                paths.append(ROOT / line.strip())
            return paths
    return []


def read_files() -> List[Course]:
    course_directories = [x for x in ROOT.iterdir() if x.is_dir() and x not in ignored_courses()]
    _courses = [Course(path) for path in course_directories]
    return sorted(_courses, key=lambda c: c.name)


class Courses(list):
    def __init__(self):
        list.__init__(self, read_files())

    @property
    def current(self) -> Course:
        return Course(CURRENT_COURSE_ROOT.resolve())

    @current.setter
    def current(self, course):
        CURRENT_COURSE_SYMLINK.unlink()
        CURRENT_COURSE_SYMLINK.symlink_to(course.path)
        CURRENT_COURSE_WATCH_FILE.write_text('{}\n'.format(course.info['short']))

from file_list import Files
from pathlib import Path
from typing import Dict


class ExerciseWriteUp:
    def __init__(self, root_dir: Path, course):
        self.root_dir = root_dir
        self.course = course
        self.number = 1

    def edit(self):
        pass


class Exercise:
    def __init__(self, course, number: int):
        self.course = course
        self.number = number
        self._writeup = None
        self._problem = None
        self._solution = None

    @property
    def writeup(self):
        if not self._writeup:
            self._writeup = next((w for w in self.course.writeups if w.number == self.number), None)
        return self._writeup

    @property
    def problem(self):
        if not self._problem:
            self._problem = next((p for p in self.course.problems if p.number == self.number), None)
        return self._problem

    @property
    def solution(self):
        if not self._solution:
            self._solution = next((s for s in self.course.solutions if s.number == self.number), None)
        return self._solution


class Exercises(list):
    def __init__(self, course):
        self.course = course
        self.info: Dict = course.info['exercises']
        self.root: Path = course.path / self.info['path']
        self.sheet_root = self.root / self.info['sheets'].strip()
        self.solutions_root = self.root / self.info['solutions'].strip()
        self.root.mkdir(parents=True, exist_ok=True)
        self.sheet_root.mkdir(parents=True, exist_ok=True)
        self.solutions_root.mkdir(parents=True, exist_ok=True)
        self._solutions = None
        self._writeups = None
        self._sheets = Files(self.sheet_root)
        list.__init__(self, (Exercise(self.course, num) for num in map(lambda s: s.number, self._sheets)))

    @property
    def sheets(self):
        return self._sheets

    @property
    def solutions(self):
        if not self._solutions:
            self._solutions = Files(self.solutions_root)
        return self._solutions

    @property
    def writeups(self):
        if not self._writeups:
            dirs = (d for d in self.root.iterdir()
                    if d.root is not self.sheet_root.root and d.root is not self.solutions_root.root)
            self._writeups = sorted((ExerciseWriteUp(d, self.course) for d in dirs), key=lambda e: e.number)
        return self._writeups

    def read_write_up_dirs(self):
        dirs = self.root.iterdir()
        return sorted((ExerciseWriteUp(d, self.course) for d in dirs if d is not self.sheets), key=lambda e: e.number)

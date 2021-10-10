from file_list import Files, FileHandle, FileType
from pathlib import Path
from typing import Dict
from utils import normalize
from config import NEW_EXERCISE_SHEET_HEADER


class ExerciseWriteUp(FileHandle):
    def __init__(self, root_dir: Path, course):
        self.root_dir = root_dir
        self.course = course
        FileHandle.__init__(self, next(self.root_dir.rglob('*.tex')), FileType.tex)


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
        self.ignored_folders = [self.sheet_root, self.solutions_root]
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
            dirs = list(d for d in self.root.iterdir() if d.is_dir() and d not in self.ignored_folders)
            self._writeups = sorted((ExerciseWriteUp(d, self.course) for d in dirs), key=lambda e: e.number)
        return self._writeups

    @staticmethod
    def __generate_name(name: str):
        return normalize(name.split(' ')[-1])

    def __generate_names(self):
        names = self.info['name']
        if type(names) == str:
            return self.__generate_name(names)
        elif type(names) == list:
            return '_'.join(map(self.__generate_name, names))

    def new_writeup(self):
        new_num = max(self.writeups, key=lambda w: w.number).number + 1
        new_dir = self.root / 'ub{num}'.format(num=new_num)
        new_dir.mkdir(parents=True, exist_ok=False)
        new_file = new_dir / '{names}_{course}_sheet_{num}.tex'.format(
            names=self.__generate_names(),
            course=normalize(self.course.info['short']),
            num=new_num
        )
        new_file.write_text(NEW_EXERCISE_SHEET_HEADER.format(
            language='ngerman' if self.course.info['language'] == 'german' else 'english',
            author=self.info['name'] if type(self.info['name']) == str else ', '.join(self.info['name']),
            course=self.course.info['title'],
            number=new_num
        ))
        return ExerciseWriteUp(new_dir, self.course)

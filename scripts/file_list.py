#!/usr/bin/python3
import re
import subprocess
import warnings
from pathlib import Path
from window_subprocess import open_pdf


class FileHandle:
    def __init__(self, file_path: Path):
        self.path = file_path
        match = re.match(r'[\D]*(\d+)[\D]*\.pdf', file_path.name)
        if match is None:
            warnings.warn(f'Invalid format in file {str(file_path)}: Could not parse number.')
            self.number = -1
        else:
            self.number = int(match.group(1))
    
    def open(self):
        open_pdf(self.path)


class Files(list):
    def __init__(self, root_path: Path, pattern: str = "*"):
        self.root: Path = root_path
        list.__init__(self, self.read_files(pattern))

    def read_files(self, pattern):
        files = self.root.glob(pattern)
        return sorted((FileHandle(f) for f in files), key=lambda f: f.number)

    def unite_files(self, name):
        result = subprocess.run(
            ['pdfunite'] + list(map(lambda f: str(f.path), self)) + [str(self.root / name)]
        )
        print(result.stdout)

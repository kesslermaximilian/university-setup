#! /usr/bin/python3

import subprocess
from pathlib import Path
import os


def edit(filepath: Path, rootpath: Path = None, env=os.environ):
    if not rootpath:
        rootpath = filepath
    subprocess.Popen([
        "termite",
        "-e",
        f"vim --servername tex-vorlesung --remote-silent {str(filepath)}"
    ], env=env, cwd=str(rootpath))

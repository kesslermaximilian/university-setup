#! /usr/bin/python3

import subprocess
from pathlib import Path
import os


def edit(filepath: Path, rootpath: Path = None, env=os.environ, servername='tex lecture'):
    if not rootpath:
        rootpath = filepath.root
    subprocess.Popen([
        "termite",
        "-e",
        f"vim --servername {servername} --remote-silent {str(filepath)}"
    ], env=env, cwd=str(rootpath))


def open_pdf(filepath: Path):
    result = subprocess.run(
        ['zathura', str(filepath)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode

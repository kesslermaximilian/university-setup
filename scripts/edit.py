#! /usr/bin/python3

import subprocess
from pathlib import Path


def edit(filepath: Path):
    subprocess.Popen([
        "termite",
        "-e",
        f"vim --servername tex-vorlesung --remote-silent {str(filepath)}"
    ])

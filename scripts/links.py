import subprocess
from typing import Dict, List


class Links:
    def __init__(self, course):
        self.course = course  # A course
        self.info: Dict = course.info['links']

    def open(self, key: str):
        self.open_link_in_browser(self.info[key])

    def available(self) -> List[str]:
        return [key for key in self.info.keys() if self.info[key] != '']

    @staticmethod
    def open_link_in_browser(url):
        result = subprocess.run(
            ['qutebrowser', str(url)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

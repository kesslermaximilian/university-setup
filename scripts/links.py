import subprocess


class Links:
    def __init__(self, course):
        self.course = course  # A course
        self.info = course.info['links']

    def open(self, key: str):
        self.open_link_in_browser(self.info[key])

    @staticmethod
    def open_link_in_browser(url):
        result = subprocess.run(
            ['qutebrowser', str(url)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

from pathlib import Path
import pytz
# default is 'primary', if you are using a separate calendar for your course schedule,
# your calendarId (which you can find by going to your Google Calendar settings, selecting
# the relevant calendar and scrolling down to Calendar ID) probably looks like
# xxxxxxxxxxxxxxxxxxxxxxxxxg@group.calendar.google.com
# example:
# USERCALENDARID = 'xxxxxxxxxxxxxxxxxxxxxxxxxg@group.calendar.google.com'
USERCALENDARID = 'primary'
CURRENT_COURSE_SYMLINK = Path('~/current_course').expanduser()
CURRENT_COURSE_ROOT = CURRENT_COURSE_SYMLINK.resolve()
CURRENT_COURSE_WATCH_FILE = Path('/tmp/current_course').resolve()
ROOT = Path('~/Uni/semester-5').expanduser()
DATE_FORMAT = '%a %d %b %Y'
LOCALE = "de_DE.utf8"
COURSE_IGNORE_FILE = '.courseignore'
COURSE_INFO_FILE_NAME = 'info.yaml'
MAX_LEN = 40
LECTURE_START_MARKER = 'start lectures'
LECTURE_END_MARKER = 'end lectures'
DEFAULT_NEW_LECTURE_HEADER = r'\lecture[]{{{date}}}{{{title}}}'
DEFAULT_NEW_LECTURE_TITLE = 'Untitled'
DEFAULT_LECTURE_SEARCH_REGEX = r'lecture.*({\d*})?{(.*?)}{(.*)}'
DEFAULT_IMPORT_INDENTATION = 4
FALLBACK_COURSE_INFO_FILE = Path(__file__).parent.resolve() / 'fallback.yaml'
TIMEZONE = pytz.timezone('CET')
SCHEDULER_DELAY = 60
DEFAULT_LATEX_COUNTER_AUX_FILE_EXTENSION = '.cnt'

NEW_EXERCISE_SHEET_HEADER = '\n'.join([
    r"%! TEX root = ./*.tex",
    r"\documentclass[{language}]{{mkessler-sheet}}",
    "",
    r"\usepackage{{babel}}",
    r"\usepackage{{mkessler-math}}",
    r"\usepackage{{mkessler-enumerate}}",
    r"\usepackage{{mkessler-figures}}",
    "",
    r"\author{{{author}}}",
    r"\course{{{course}}}",
    r"\sheetnumber{{{number}}}",
    "",
    r"\begin{{document}}",
    r"\maketitle",
    "",
    "",
    r"\end{{document}}"
])

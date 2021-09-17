from pathlib import Path

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
COURSE_INFO_FILE = 'info.yaml'
DEFAULT_MASTER_FILE_NAME = 'master.tex'
MAX_LEN = 40
LECTURE_START_MARKER = 'start lectures'
LECTURE_END_MARKER = 'end lectures'
DEFAULT_NEW_LECTURE_HEADER = r'\lecture{{{number}}}{{{date}}}{{{title}}}'
DEFAULT_LECTURE_SEARCH_REGEX = r'lecture{(.*?)}{(.*?)}{(.*)}'
DEFAULT_IMPORT_INDENTATION = 4

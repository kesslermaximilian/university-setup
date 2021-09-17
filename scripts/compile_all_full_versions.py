#!/bin/python3
from courses import Courses

for course in Courses():
    notes = course.notes
    if notes.full_file:
        notes.compile_full()
        continue
    else:
        lectures = notes.lectures
        r = lectures.parse_range_string('all')
        notes.update_lectures_in_master(r)
        notes.compile_master()

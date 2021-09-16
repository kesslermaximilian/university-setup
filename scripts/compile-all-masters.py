#!/bin/python3
from courses import Courses

for course in Courses():
    script = course.notes
    lectures = script.lectures

    r = lectures.parse_range_string('all')
    script.update_lectures_in_master(r)
    script.compile_master()

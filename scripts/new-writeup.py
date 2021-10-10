#! /usr/bin/python3
from courses import Courses

course = Courses().current
writeup = course.exercises.new_writeup()
writeup.edit()

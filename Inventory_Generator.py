from canvas_apps.connect import connect
from canvas_apps.util.data import course_inventory

import csv

COURSE_DATA_FOLDER = 'course_data'
COURSE_DATA_FILE = COURSE_DATA_FOLDER + '/courses.csv'

canvas = connect()

with open(COURSE_DATA_FILE, 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        course = canvas.get_course(row['id'])
        if course_inventory(course, 'course_data'):
            print(f'{course.name} ({course.id}) successfully inventoried.')
        else:
            print(f'Error while creating a course inventory for {course.name} ({course.id}).')


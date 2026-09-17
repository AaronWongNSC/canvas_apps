from canvas_apps.connect import connect
from canvas_apps.util.data import paginated_to_dict, dict_str_match

import csv
from pathlib import Path

COURSE_DATA_FOLDER = 'course_data'
COURSE_DATA_FILE = COURSE_DATA_FOLDER + '/courses.csv'

## Check if the course_data folder exists. Create it if it doesn't.
folder_path = Path(COURSE_DATA_FOLDER)
folder_path.mkdir(parents=True, exist_ok=True)

## Get full list of courses
canvas = connect()
courses = paginated_to_dict(canvas.get_courses())

## Check if a courses.csv file exists. Load it if it does.
file_path = Path(COURSE_DATA_FILE)

my_courses = {}
if file_path.is_file():
    print('This is the current list of courses in your file:')

    with open(COURSE_DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)

        for count, row in enumerate(reader):
            print(f'{count}:\t{row['name']} ({row['id']})')
            my_courses[row['id']] = row['name']


## Search for string
search_string = input('Enter the search string for the course titles: ')
matches = dict_str_match(courses, 'name', search_string)

if matches:
    ## If matches found, determine whether to add or replace
    print('Matches Found: ')
    for course in matches:
        print(f'{course['name']} ({course['id']})')

    choice = input('[A]dd these courses to the list, [R]eplace the list with these courses, or anything else to exit: ').upper()

    print(choice)

    if choice == 'R':
        my_courses = {}
    if choice in ['A', 'R']:
        for course in matches:
            my_courses[course['id']] = course['name']

    ## Update the courses.csv file
    with open(COURSE_DATA_FILE, 'w') as file:
        file.write('id,name\n')
        for id, name in my_courses.items():
            file.write(f'{id},{name}\n')

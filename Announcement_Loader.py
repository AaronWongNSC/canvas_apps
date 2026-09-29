import canvas_apps.error

from canvas_apps.connect import connect, get_course, disconnect
from canvas_apps.util.data import commas, load_announcements
from canvas_apps.util.date import local_date_time_to_ztime, split_ztime

from pathlib import Path

import csv

## Connect to Canvas
canvas = connect()

# Menu
print('''
Choose from the following options:

1) Download announcements from course
2) Upload and schedule announcements to course
''')
command = int(input('Selection: '))
if command not in [1, 2]:
    raise ValueError("Invalid selection.")

## Download Announcements
if command == 1:
    # Load announcement data
    course = get_course(canvas)
    announcements = load_announcements(canvas, course)

    with open(f'Announcements-{course.name}.csv', 'w') as out_file:
        out_file.write('course_id,course_name,announcement_id,title,post_date,post_time\n')
        for annoucement, contents in announcements.items():
            post_date, post_time = split_ztime(contents['posted_at'])
            out_file.write(commas([course.id, course.name, contents['id'], contents['title'], post_date, post_time]))

    print(f'''
You should find a file called "Announcements.csv" in this folder. Enter the date (MM/DD/YY or MM/DD/YYYY)
and time (24-hour HH:MM) when you want the announcement to be posted. If you do not want to post an announcement,
simply eliminate that row.

You can also review the contents of the announcements in the "Announcements.json" file and make manual edits,
as necessary. If you change the title of the announcement, you will need to update the CSV file to match it. Note that
HTML links may not function correctly if they link to a different course.
''')

## Upload Announcements
elif command == 2:
    ## Get file
    files = []
    for index, filename in enumerate(list(Path('./').glob('*.csv'))):
        print(f'{index}: {filename}')
        files.append(filename)

    choice = int(input('Select a file: '))
    filename = files[choice]

    ## Get destination course
    print('--- Select the destination course for the announcements --- ')
    destination_course = get_course(canvas)


    with open(filename, 'r') as in_file:
        reader = csv.DictReader(in_file)

        for row in reader:
            post_z = local_date_time_to_ztime(row['post_date'], row['post_time'])
            source_course = canvas.get_course(row['course_id'])
            source_announcements = load_announcements(canvas, source_course)
            announcement = source_announcements[str(row['announcement_id'])]
            html = announcement['message']

            destination_course.create_discussion_topic(
                title = row['title'],
                message = html,
                is_announcement = True,
                delayed_post_at = post_z
            )

            print(f'Scheduling {row['title']} for {row['post_date']} at {row['post_time']}')

disconnect()
import canvas_apps.error

from canvas_apps.connect import connect, get_course
from canvas_apps.ui import display_message, prompt
from canvas_apps.util.data import commas, load_announcements
from canvas_apps.util.date import local_date_time_to_ztime, split_ztime

from pathlib import Path

import csv

def announcement_loader():

    ## Connect to Canvas
    canvas = connect()

    while True:
        # Menu
        selection = prompt([
                '(1) Download announcements from course',
                '(2) Upload and schedule announcements',
                '(X) Exit Tool'
            ])

        if selection == '1': ## Download Announcements
            # Load announcement data
            course = get_course(canvas)
            announcements = load_announcements(canvas, course)

            with open(f'Announcements-{course.name}.csv', 'w') as out_file:
                out_file.write('course_id,course_name,announcement_id,title,post_date,post_time\n')
                for annoucement, contents in announcements.items():
                    post_date, post_time = split_ztime(contents['posted_at'])
                    out_file.write(commas([course.id, course.name, contents['id'], contents['title'], post_date, post_time]))

            print(f'''
You should find a file called "Announcements-{course.name}.csv" in this folder. Enter the date (MM/DD/YY or MM/DD/YYYY)
and time (24-hour HH:MM) when you want the announcement to be posted. If you do not want to post an announcement,
simply eliminate that row.

You can also review the contents of the announcements in the "{course.id}-announcements.json" file and make manual edits,
as necessary. If you change the title of the announcement, you will need to update the CSV file to match it. Note that
HTML links may not function correctly if they link to a different course.
        ''')

        
        if selection == '2': ## Upload Announcements
            ## Get file
            selection = int(prompt(
                [ f'({index}) {filename}' for index, filename in enumerate(list(Path('./').glob('*.csv'))) ],
                title='Select the CSV file with the announcement list'))
            filename = list(Path('./').glob('*.csv'))[selection]

            ## Get destination course
            print('\n--- Select the destination course for the announcements --- ')
            destination_course = get_course(canvas)

            display_message('Loading announcements')
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

                    print(f'Scheduling "{row['title']}" for {row['post_date']} at {row['post_time']}')
            display_message('Task complete!')

        if selection == 'X': ## Exit
            break

if __name__ == "__main__":
    announcement_loader()
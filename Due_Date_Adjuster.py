import canvas_apps.error

from canvas_apps.connect import connect, get_course
from canvas_apps.ui import display_long_message, display_message, prompt
from canvas_apps.util.data import dict_str_match, commas, load_assignments
from canvas_apps.util.date import split_ztime, local_date_time_to_ztime, ztime_to_local

import csv

def due_date_adjuster():
    ## Connect to Canvas
    canvas = connect()
    course = get_course(canvas)

    ## Load assignment data
    assignments = load_assignments(course)

    while True:

        # Menu
        selection = prompt([
            '(1) Generate CSV file',
            '(2) Update Assignment Dates',
            '(X) Exit Tool'
        ],
        title='DUE DATE ADJUSTER')

        ## Download assignments
        if selection == '1':
            with open(f'{course.id}-Assignments.csv', 'w') as out_file:
                out_file.write('assignment_name,unlock_date,unlock_time,due_date,due_time,lock_date,lock_time\n')
                for _, assignment in assignments.items():
                    if assignment['unlock_at']:
                        unlock_date, unlock_time = split_ztime(assignment['unlock_at'])
                    else:
                        unlock_date = ''
                        unlock_time = ''

                    if assignment['due_at']:
                        due_date, due_time = split_ztime(assignment['due_at'])
                    else:
                        due_date = ''
                        due_time = ''

                    if assignment['lock_at']:
                        lock_date, lock_time = split_ztime(assignment['lock_at'])
                    else:
                        lock_date = ''
                        lock_time = ''

                    out_file.write(commas([assignment['name'],
                                        unlock_date, unlock_time,
                                        due_date, due_time,
                                        lock_date, lock_time]))
            display_long_message([
                f'A file called "{course.id}-Assignments.csv" has been created in this folder. Enter the date (MM/DD/YY or MM/DD/YYYY)',
                'and time (24-hour HH:MM) when you want the assignments to be unlocked, due, or locked. Blank dates will clear the',
                'unlock/due/lock date. Blank times will be set to 23:59 (end of the day).',
                '',
                'Changing the name of the assignment will cause the program to malfunction.',
            ])
        ## Update assignments
        if selection == '2':
            display_message(f'Updating due dates from {course.id}-Assignments.csv')
            with open(f'{course.id}-Assignments.csv', 'r') as in_file:
                reader = csv.DictReader(in_file)

                for row in reader:
                    if row['assignment_name'].strip() == '':
                        continue

                    ## Set midnight times for non-existent times
                    if row['unlock_time'].strip() == '':
                        row['unlock_time'] = '23:59'
                    if row['due_time'].strip() == '':
                        row['due_time'] = '23:59'
                    if row['lock_time'].strip() == '':
                        row['lock_time'] = '23:59'

                    ## Create z_time objects
                    if row['unlock_date'].strip():
                        unlock_at = local_date_time_to_ztime(row['unlock_date'], row['unlock_time'])
                        unlock_at_local = ztime_to_local(unlock_at)
                    else:
                        unlock_at = ''
                        unlock_at_local = '(None)'

                    if row['due_date'].strip():
                        due_at = local_date_time_to_ztime(row['due_date'], row['due_time'])
                        due_at_local = ztime_to_local(due_at)
                    else:
                        due_at = ''
                        due_at_local = '(None)'

                    if row['lock_date'].strip():
                        lock_at = local_date_time_to_ztime(row['lock_date'], row['lock_time'])
                        lock_at_local = ztime_to_local(lock_at)
                    else:
                        lock_at = ''
                        lock_at_local = '(None)'

                    ## Update
                    assignment = dict_str_match(assignments, 'name', row['assignment_name'])[0]
                    assignment = course.get_assignment(assignment['id'])
                    assignment.edit(
                        assignment = {
                            'unlock_at': unlock_at,
                            'due_at': due_at,
                            'lock_at': lock_at,
                        }
                    )

                    ## Display
                    print(f'Updating {assignment.name} - Unlock: {unlock_at_local} / Due: {due_at_local} / Lock: {lock_at_local}')
            display_message(f'Task complete!')
        if selection == 'X':
            break

if __name__ == "__main__":
    due_date_adjuster()
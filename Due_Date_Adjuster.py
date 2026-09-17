from canvas_apps.connect import connect, disconnect, get_course
from canvas_apps.util.data import inventory, json_read, dict_str_match, commas
from canvas_apps.util.date import split_ztime, local_date_time_to_ztime, ztime_to_local

import csv

## Connect to Canvas
canvas = connect()
course = get_course(canvas)

## Load assignment data
assignments = json_read(f'course_data/{course.id}-assignments')

# Menu
print('''
Choose from the following options:

1) Generate CSV file
2) Update assignment dates
''')
command = int(input('Selection: '))
if command not in [1, 2]:
    raise ValueError("Invalid selection.")

## Download assignments
if command == 1:
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
    print(f'''
You should find a file called "{course.id}-Assignments.csv" in this folder. Enter the date (MM/DD/YY or MM/DD/YYYY)
and time (24-hour HH:MM) when you want the assignments to be unlocked, due, or locked. Blank dates will clear the
unlock/due/lock date. Blank times will be set to 23:59 (end of the day).

Eliminating a row will cause that assignment to be left unchanged.
''')
## Update assignments
elif command == 2:
    with open(f'{course.id}-Assignments.csv', 'r') as in_file:
        reader = csv.DictReader(in_file)

        for row in reader:

            ## Set midnight times for non-existent times
            if row['unlock_time'] == '':
                row['unlock_time'] = '23:59'
            if row['due_time'] == '':
                row['due_time'] = '23:59'
            if row['lock_time'] == '':
                row['lock_time'] = '23:59'

            ## Create z_time objects
            if row['unlock_date']:
                unlock_at = local_date_time_to_ztime(row['unlock_date'], row['unlock_time'])
                unlock_at_local = ztime_to_local(unlock_at)
            else:
                unlock_at = ''
                unlock_at_local = '(None)'

            if row['due_date']:
                due_at = local_date_time_to_ztime(row['due_date'], row['due_time'])
                due_at_local = ztime_to_local(due_at)
            else:
                due_at = ''
                due_at_local = '(None)'

            if row['lock_date']:
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
            print(f'Updatng {assignment.name} - Unlock: {unlock_at_local} / Due: {due_at_local} / Lock: {lock_at_local}')

disconnect()
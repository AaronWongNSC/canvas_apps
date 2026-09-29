import canvas_apps.error

from canvas_apps.connect import connect, get_course
from canvas_apps.util.data import load_users, load_assignments
from canvas_apps.util.date import ztime_to_local

## Connect to Canvas
canvas = connect()
course = get_course(canvas)

## Load user and assignment data
users = load_users(course)
assignments = load_assignments(course)

## Preparation
assignments = [ assignment for _, assignment in assignments.items() if assignment['due_at'] is not None]

participation = {
    student['id']: {
        'name': student['name'],
        'due_date': None,
        'submission': None
    } for _, student in users.items()
}

## Main loop
count = 1
for assignment in assignments:
    print(f'{assignment['name']} -- ({count}/{len(assignments)})')
    submissions = course.get_assignment(assignment['id']).get_submissions()

    for submission in submissions:
        try:
            if submission.score > 0:
                if not participation[submission.user_id]['due_date']:
                    participation[submission.user_id]['due_date'] = assignment['due_at']
                else:
                    if participation[submission.user_id]['due_date'] < assignment['due_at']:
                        participation[submission.user_id]['due_date'] = assignment['due_at']
                if not participation[submission.user_id]['submission']:
                    participation[submission.user_id]['submission'] = submission.submitted_at
                else:
                    if participation[submission.user_id]['submission'] < submission.submitted_at:
                        participation[submission.user_id]['submission'] = submission.submitted_at
        except:
            pass
    count += 1

with open(f'Last-Participation-{course.id}-{course.name}.csv', 'w') as out_file:
    out_file.write('Student,Last Due Date,Last Submission\n')
    for _, student in participation.items():
        last_due_date = 'N/A'
        last_submission = 'N/A'
        
        if student['due_date']:
            last_due_date = ztime_to_local(student['due_date'])
        if student['submission']:
            last_submission = ztime_to_local(student['submission'])
        out_file.write(f'{student['name']},{last_due_date},{last_submission}\n')
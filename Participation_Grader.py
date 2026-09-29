import canvas_apps.error

from canvas_apps.connect import connect, get_course
from canvas_apps.ui import get_ids_from_dict, sift_sort
from canvas_apps.util.data import load_assignments, load_users

from pathlib import Path

## Connect to Canvas
canvas = connect()
course = get_course(canvas)

## Load user and assignment data
users = load_users(course)
assignments = load_assignments(course)

# Get the assignment and submissions
assignments = sift_sort(assignments, 'name', 'due_at')
assignment_ids = get_ids_from_dict(assignments)

for assignment_id in assignment_ids:
    assignment = course.get_assignment(assignment_id)
    submissions = assignment.get_submissions()

    print(f'Grading {assignment.name}')

    ## BEGIN GRADING
    for submission in submissions:
        points_possible = assignment.points_possible
        student_name = users[str(submission.user_id)]['name']
        if submission.attempt:
            print(f'Grading Submission for {users[str(submission.user_id)]['name']}')
            submission.edit(submission={'posted_grade': points_possible})
        else:
            print(f'No Submission for {users[str(submission.user_id)]['name']}')
            submission.edit(submission={'posted_grade': 0})
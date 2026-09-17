from canvas_apps.connect import connect, get_course
from canvas_apps.ui import get_id_from_file, get_id_from_dict, sift_sort
from canvas_apps.util.data import paginated_to_dict, json_read, inventory

from pathlib import Path

## Connect to Canvas
canvas = connect()
course = get_course(canvas)

## Load user and assignment data
users = json_read(f'course_data/{course.id}-users')
assignments = json_read(f'course_data/{course.id}-assignments')

# Get the assignment and submissions
assignments = sift_sort(assignments, 'name', 'due_at')
assignment_id = get_id_from_dict(assignments)
assignment = course.get_assignment(assignment_id)
submissions = assignment.get_submissions()

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
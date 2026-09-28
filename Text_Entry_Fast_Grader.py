from canvas_apps.connect import connect, disconnect, get_course
from canvas_apps.util.data import load_assignments, load_users
from canvas_apps.util.html import cleanse, deTeX

from pathlib import Path
from bs4 import BeautifulSoup

import json

## Connect to Canvas
canvas = connect()
course = get_course(canvas)

## Load user and assignment data
users = load_users(course)
print(users)
assignments = load_assignments(course)

## Sift/sort assignments
assignments = {
    id: assignment for id, assignment in assignments.items()
        if assignment['due_at'] is not None and assignment['submission_types'] == ['online_text_entry']
}

assignments = dict(sorted(assignments.items(), key=lambda item: item[1]['due_at']))

# Get the assignment_id
assignment_list = []
count = 0
for id, assignment in assignments.items():
    print(f'{count}: {assignment['name']} ({assignment['due_at']})')
    assignment_list.append(id)
    count += 1 

selection = int(input('Select an assignment: '))
assignment_id = assignment_list[selection]

## Load Canvas Data
assignment = course.get_assignment(assignment_id)
submissions = assignment.get_submissions()

for submission in submissions:
    ## Reset values
    try:
        student_name = users[str(submission.user_id)]['name']
    except:
        print('Skipping unenrolled student')
        continue

    points_possible = assignment.points_possible
    
    current_score = submission.score
    grade_change = False
    score = None
    comment = None
    default = None
    response = None
    prompt = None

    current_text = ''
    comment_text = ''

    if current_score:
        current_text = f'(Current score: {current_score}/{points_possible})'

    print()
    print(f'--------- Submission for {student_name} {current_text}')

    if submission.attempt:
        soup = BeautifulSoup(deTeX(cleanse(submission.body)), 'html.parser')
        response = soup.text

        if current_score:
            prompt = '[Enter] for no change, [score]|[comment] to update the score with comment: '
        else:
            prompt = '[Enter] for full credit with no comment, [score]|[comment] for specific score with comment, [X] to skip: '
            default = points_possible
    else:
        prompt = '[Enter] for no credit with no comment, [score]|[comment] for specific score with comment, [X] to skip: '
        response = '[No Submission]'
        default = 0

    print(response + '\n')
    grade = input(prompt)
        
    if grade == '':
        if default is not None:
            grade_change = True
            score = default
    elif grade == 'X':
        pass
    else:
        grade_change = True
        if '|' in grade:
            grade_change = True
            score, comment = grade.split('|')
        else:
            score = grade

    if grade_change:
        if comment:
            comment_text = f' with comment: {comment}'
        submission.edit(
            submission={'posted_grade': score},
            comment={'text_comment': comment})
        print(f'\n *** Grade updated to {score}/{points_possible} {comment_text}')
    else:
        print(f'\n *** No grade change for {student_name}')

disconnect()
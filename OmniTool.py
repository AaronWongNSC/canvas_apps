from canvas_apps import error
from pathlib import Path
from canvas_apps.ui import prompt

from Announcement_Loader import announcement_loader
from Discussion_Post_Counter import discussion_post_counter
from Due_Date_Adjuster import due_date_adjuster
from Last_Participation_Checker import last_participation_checker
from Participation_Grader import participation_grader
from Setup_Tool import setup_tool
from Text_Entry_Fast_Grader import text_entry_fast_grader


### Check for folders
folder_path = Path('config')
folder_path.mkdir(parents=True, exist_ok=True)

folder_path = Path('course_data')
folder_path.mkdir(parents=True, exist_ok=True)


### MAIN MENU
while True:
    selection = prompt([
        '(1) Setup Tool -- Run this first!',
        '(2) Due Date Adjuster -- Adjust due dates using a CSV file',
        '(3) Last Participation Checker -- Identify the last date of participation',
        '(4) Announcement Loader -- Load and schedule announcements',
        '(5) Discussion Post Counter -- Quickly count the number of posts by each student in each discussion',
        '(6) Participation Grader -- Grade assignments based on participation',
        '(7) Text Entry Fast Grader -- Quickly grade text entry assignments',
        '(X) Exit Program'
    ], title = 'Welcome to the OmniTool!')

    if selection == '1':
        setup_tool()
    if selection == '2':
        due_date_adjuster()
    if selection == '3':
        last_participation_checker()
    if selection == '4':
        announcement_loader()
    if selection == '5':
        discussion_post_counter()
    if selection == '6':
        participation_grader()
    if selection == '7':
        text_entry_fast_grader()
    if selection == 'X':
        break

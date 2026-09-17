"""
Main connection scripts
"""

from canvasapi import Canvas
from canvasapi.course import Course

from canvas_apps.ui import get_id_from_file

def connect(INSTITUTION:str = 'nevadastate') -> Canvas:
    """Begins the connection protocol to Canvas through canvasapi.

    1) Request the connection type (test, beta, main/production)
    2) Check for an API key for the given connection (filenames: test_key.txt, beta_key.txt, main_key.txt)
    3) Test the connection

    Parameters
    ----------
    INSTITUTION
        Institutional name for the URL (INSTITUTION.instructure.com)

    Returns
    -------
    Canvas
        A logged-in Canvas instance (or an error message if something went wrong)
    """

    ## Connection Selection
    choice = ''
    while choice not in [1, 2, 3]:
        print('\nConnection Options:')
        print(f'1) {INSTITUTION}.test.instructure.com (API_KEY file: test_key.txt)')
        print(f'2) {INSTITUTION}.beta.instructure.com (API_KEY file: beta_key.txt)')
        print(f'3) {INSTITUTION}.instructure.com (API_KEY file: main_key.txt)')
        choice = int(input('Select a connection: '))

    if choice == 1:
        API_URL = f'https://{INSTITUTION}.test.instructure.com'
        key_file = 'test_key.txt'
    if choice == 2:
        API_URL = f'https://{INSTITUTION}.beta.instructure.com'
        key_file = 'beta_key.txt'
    if choice == 3:
        print('\n ----- WARNING: YOU ARE ABOUT TO EDIT STUDENT-FACING DATA ----- \n')
        test = input('Type "confirm" to confirm that you want to do this: ')
        if not test.strip().upper() == 'CONFIRM':
            disconnect()
        API_URL = f'https://{INSTITUTION}.instructure.com'
        key_file = 'main_key.txt'
        
    ## Get API_KEY from file
    try:
        with open(key_file, 'r') as file:
            API_KEY = file.read().strip()
    except:
        ### Print instructions
        print(f'ERROR: {key_file} not found.')
        print(f'''
To get an API key:
1) Log into the appropriate Canvas instance
2) Click "Account" (at the top-left corner)
3) Select "Settings"
4) Click the blue "+ New Access Token" button
5) Enter a purpose (this can be anything), and an expiration date and time (typically a week or two in the future)
6) Click "Generate Token"
7) A window will pop up with your API key next to "Token" (it is the long string of text)
8) Copy this into a plain text file in this folder. Use the filename {key_file}.

''')
        disconnect()

    ### Test Connection
    try:
        canvas = Canvas(API_URL, API_KEY)
        canvas.get_current_user()
        print('Connection successful!')
        return canvas
    except Exception as e:
        print(f'An error occurred: {e}')
        disconnect()

def get_course(canvas:Canvas) -> Course:
    course_id = get_id_from_file('course_data/courses.csv')
    if course_id == False:
        course_id = int(input('Enter the Course ID: '))
    return canvas.get_course(course_id)

def disconnect():
    import sys

    input('Press [Enter] to exit...')
    sys.exit()
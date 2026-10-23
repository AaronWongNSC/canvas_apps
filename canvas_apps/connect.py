"""
Main connection scripts
"""

from canvasapi import Canvas
from canvasapi.course import Course

from canvas_apps.config import load_config, update_key
from canvas_apps.ui import display_message, get_id_from_list, prompt

def connect() -> Canvas:
    """Begins the connection protocol to Canvas through canvasapi.

    1) Request the connection type (test, beta, main/production)
    2) Check for an API key for the given connection (located in config/config.json)
    3) Test the connection

    Parameters
    ----------
    None

    Returns
    -------
    Canvas
        A logged-in Canvas instance (or an error message if something went wrong)
    """

    config = load_config()
    institution = config['prefix']
    
    ## Connection Selection
    while True:
        selection = prompt([
            f'(1) {institution}.test.instructure.com',
            f'(2) {institution}.beta.instructure.com',
            f'(3) {institution}.instructure.com'
        ])

        if selection == '1':
            API_URL = f'https://{institution}.test.instructure.com'
            key = config['test_key']['key']
            if key is None:
                key = update_key('test_key')['key']
            API_KEY = key
        
        if selection == '2':
            API_URL = f'https://{institution}.beta.instructure.com'
            key = config['beta_key']['key']
            if key is None:
                key = update_key('beta_key')['key']
            API_KEY = key
        if selection == '3':
            print('\n ----- WARNING: YOU ARE ABOUT TO EDIT STUDENT-FACING DATA ----- \n')
            test = input('Type "confirm" to confirm that you want to do this: ')
            if not test.strip().upper() == 'CONFIRM':
                break
            API_URL = f'https://{institution}.instructure.com'
            key = config['main_key']['key']
            if key is None:
                key = update_key('main_key')['key']
            API_KEY = key
        
        ## Get API_KEY from file
        if not API_KEY:
            ### Print instructions
            display_message('ERROR: API_KEY not found.')
            break

        ### Test Connection
        try:
            canvas = Canvas(API_URL, API_KEY)
            canvas.get_current_user()
            display_message('Connection successful!')
            return canvas
        except Exception as e:
            display_message(f'An error occurred: {e}')
            disconnect()

def get_course(canvas:Canvas) -> Course:
    """Creates a canvasapi Course object from a list of courses.

    Parameters
    ----------
    canvas: Canvas
        A canvas instance

    Returns
    -------
    Course
        A Course instance
    """
    config = load_config()
    if len(config['course_list']) == 0:
        display_message('No courses available -- Run the setup tool to create a course list')
        return None

    course_id = get_id_from_list(config['course_list'])
    return canvas.get_course(course_id)

def disconnect():
    import sys

    input('Press [Enter] to exit...')
    sys.exit()
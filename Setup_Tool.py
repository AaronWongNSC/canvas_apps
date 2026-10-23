from canvas_apps import error
from canvas_apps.config import load_config, save_config, update_key
from canvas_apps.connect import connect
from canvas_apps.ui import display_message, display_long_message, prompt
from canvas_apps.util.data import clear_data_files, dict_str_match, load_courses, inventory

def key_exists(key:str) -> str:
    """Helper function to display API key information

    Parameters
    ----------
    key : str
        Identifies the dictionary key with the API key information. It must be in
        ['main_key', 'beta_key', 'test_key'].

    Returns
    -------
    str
        A string describing the status of the key.
    """
    if key['key']:
        return f'Stored on {key['date']}'
    return 'Missing'

def update_course_list(course_list:list) -> list:
    """Function to manage updating the course list

    Parameters
    ----------
    course_list : list
        A list of the courses that are displayed by the setup tool.

    Returns
    -------
    list
        The updated course list
    """
    def display_courses(course_list): ## Helper tool to display the courses
        # Reindex every time!
        for index, course in enumerate(course_list):
            course['index'] = index

        if len(course_list) > 0:
            display_long_message([
                'Current Course List:',
                ''] + [f'({course['index']}) {course['name']} ({course['id']})' for course in course_list])
        else:
            print('Empty Course List')
        print()
        return

    canvas = connect()

    while True:
        display_courses(course_list)

        selection = prompt([
            '(1) Add courses',
            '(2) Remove courses',
            '(3) Update course list from Canvas',
            '(X) Exit Tool'
            ], title = 'UPDATE COURSE LIST')
        if selection == '1': ## Add courses
            courses = load_courses(canvas)
            search_string = input('Enter the search string for the course titles: ')
            matches = dict_str_match(courses, 'name', search_string)
            if matches:
                display_message('Matches found')
                for index, course in enumerate(matches):
                    print(f'({index}) {course['name']} ({course['id']})')
                add_courses = input('Select courses to add (use commas to separate values): ').split(',')
                add_courses = [ int(course_index) for course_index in add_courses]
                add_list = [ course for index, course in enumerate(matches) if index in add_courses]
                for add in add_list:
                    if add['id'] not in [ course['id'] for course in course_list ]:
                        course_list.append(add)

        if selection == '2': ## Remove courses
            if len(course_list) == 0:
                display_message('The course list is empty')
            else:
                remove_courses = input('Select courses to remove (use commas to separate values): ').split(',')
                remove_courses = [ int(course) for course in remove_courses]
                course_list = [ course for course in course_list if course['index'] not in remove_courses]

        if selection == '3': ## Update the data file from Canvas
            filename = f'course_data/courses.json'
            inventory(canvas.get_courses(), filename)

        if selection == 'X': ## Done
            break

    return course_list

def update_institution(institution:str) -> str:
    """Function to manage updating the institutional prefix

    Parameters
    ----------
    institution : str
        The institutional prefix for Canvas

    Returns
    -------
    str
        The updated institutional prefix
    """

    new_institution = prompt([
        f'Current institution URL prefix: {institution}',
        f'Main Instance: https://{institution}.instructure.com',
        f'Beta Instance: https://{institution}.beta.instructure.com',
        f'Test Instance: https://{institution}.test.instructure.com',
        ],
        title='UPDATE INSTITUIONAL PREFIX',
        prompt='Enter the new URL prefix (blank to keep the old one):').lower()
    if not new_institution:
        return institution
    return new_institution

##### MAIN CODE FOR THE SETUP TOOL
def setup_tool():
    while True:
        config = load_config()
        selection = prompt([
            f'(1) [{config['prefix']}] Institution URL Prefix',
            f'(2) [{key_exists(config['main_key'])}] Main Instance API Key',
            f'(3) [{key_exists(config['beta_key'])}] Beta Instance API Key',
            f'(4) [{key_exists(config['test_key'])}] Test Instance API Key',
            f'(5) Update course list',
            f'(6) Clear data files',
            f'(X) Exit Tool'
        ], title = 'SETUP TOOL')

        if selection == '1':
            config['prefix'] = update_institution(config['prefix'])
            save_config(config)
        if selection == '2':
            config['main_key'] = update_key('main_key')
            save_config(config)
        if selection == '3':
            config['beta_key'] = update_key('beta_key')
            save_config(config)
        if selection == '4':
            config['test_key'] = update_key('test_key')
            save_config(config)
        if selection == '5':
            config['course_list'] = update_course_list(config['course_list'])
            save_config(config)
        if selection == '6':
            clear_data_files()
        if selection == 'X':
            break

if __name__ == "__main__":
    setup_tool()
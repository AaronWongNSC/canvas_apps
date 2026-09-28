"""
Utilities to work with data
"""

from canvasapi.canvas import Canvas
from canvasapi.course import Course
from canvasapi.paginated_list import PaginatedList

from canvas_apps.util.date import local_dt_to_ztime

from datetime import datetime
from pathlib import Path

import json

def commas(values:list) -> str:
    """Prepares values to be inserted into a CSV file so that quotes and commas do not
    create problems.

    Parameters
    ----------
    values : list
        A list of data to be safely comma-separated.

    Returns
    -------
    str
        A string (including newline) ready to be added to a CSV file.
    """
    modified_values = [ f'{value}'.replace('"', '""') for value in values ]
    return ','.join([f'"{value}"' for value in modified_values]) + '\n'

def dict_str_match(search_dict:dict, search_key:str, target_value:str) -> list:
    """Searches a dictionary of dictionaries by key and returns a list of entries for which
    the target_value is a substring of the key's value.

    Parameters
    ----------
    search_dict : dict
        The dictionary to be searched.
    search_key : str
        The key to be searched by.
    target_value : str
        The substring to match by the search.

    Returns
    -------
    list
        A list containing the matching dictionary entries.
    """
    match = []
    for _, contents in search_dict.items():
        try:
            if target_value.casefold() in contents[search_key].casefold():
                match.append(contents)
        except:
            pass
    return match

def inventory(paginated: PaginatedList, filename: str, id:str = 'id') -> dict:
    """Converts a PaginatedList to a dictionary and writes the data to a file.

    Parameters
    ----------
    paginated : PaginatedList
        The paginated list to be converted to a dictionary.
    filename : str
        The name of the final inventory file.
    id : str
        The key to use as the ID for the dictionary.

    Returns
    -------
    dict
        The dictionary containing the contents of paginated.
    """
    data = paginated_to_dict(paginated, id)
    json_write(data, filename)
    print(f'{filename} inventory complete.')
    return data

def json_write(data: dict, filename: str) -> None:
    """Save a dictionary as a JSON data file.
	
    Parameters
    ----------
    data : dict
        The dictionary to be saved.
    filename : str
        The name of the file in which the data will be saved. The .json extension
		will be appended automatically if it doesn't exist.

    Returns
    -------
    None
    """
    try:
        if not filename.endswith('.json'):
              filename += '.json'
        with open(filename, 'w') as out_file:
            out_file.write(json.dumps(data, indent=4))
    except:
        print('Something went wrong!')
        import traceback
        traceback.print_exc()

def json_read(filename: str) -> dict:
    """Reads a JSON data file into a dictionary.
	
    Parameters
    ----------
    filename : str
        The name of the file from which the data will be loaded. The .json extension
        will be appended automatically if it doesn't exist.

    Returns
    -------
    dict
        A dictionary that contains the data. If the data was not loaded properly,
        the dictionary will be empty.
    """
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'r') as in_file:
        return json.load(in_file)

def load_announcements(canvas:Canvas, course:Course) -> dict:
    """Loads the announcement data. First attempt is by file, then through Canvas.
	
    Parameters
    ----------
    course: Course
        The Course from which to load the data.

    Returns
    -------
    dict
        A dictionary that contains the data.
    """
    filename = f'course_data/{course.id}-announcements.json'
    file_path = Path(filename)
    if not file_path.is_file():
        print(f'Announcement data for {course.name} ({course.id}) not found at {filename}')
        print('Downloading data from Canvas')
        start_date = course.created_at
        end_date = local_dt_to_ztime(datetime.now())
        inventory(canvas.get_announcements([course], start_date=start_date, end_date=end_date), filename)
    return json_read(filename)

def load_assignments(course:Course) -> dict:
    """Loads the assignment data. First attempt is by file, then through Canvas.
	
    Parameters
    ----------
    course: Course
        The Course from which to load the data.

    Returns
    -------
    dict
        A dictionary that contains the data.
    """
    filename = f'course_data/{course.id}-assignments.json'
    file_path = Path(filename)
    if not file_path.is_file():
        print(f'Assignment data for {course.name} ({course.id}) not found at {filename}')
        print('Downloading data from Canvas')
        inventory(course.get_assignments(), filename)
    return json_read(filename)

def load_assignment_groups(course:Course) -> dict:
    """Loads the assignment_group data. First attempt is by file, then through Canvas.
	
    Parameters
    ----------
    course: Course
        The Course from which to load the data.

    Returns
    -------
    dict
        A dictionary that contains the data.
    """
    filename = f'course_data/{course.id}-assignment_groups.json'
    file_path = Path(filename)
    if not file_path.is_file():
        print(f'Assignment group data for {course.name} ({course.id}) not found at {filename}')
        print('Downloading data from Canvas')
        inventory(course.get_assignment_groups(), filename)
    return json_read(filename)

def load_discussions(course:Course) -> dict:
    """Loads the discussion data. First attempt is by file, then through Canvas.
	
    Parameters
    ----------
    course: Course
        The Course from which to load the data.

    Returns
    -------
    dict
        A dictionary that contains the data.
    """
    filename = f'course_data/{course.id}-discussions.json'
    file_path = Path(filename)
    if not file_path.is_file():
        print(f'Discussions data for {course.name} ({course.id}) not found at {filename}')
        print('Downloading data from Canvas')
        inventory(course.get_discussion_topics(), filename)
    return json_read(filename)

def load_files(course:Course) -> dict:
    """Loads the file data. First attempt is by file, then through Canvas.
	
    Parameters
    ----------
    course: Course
        The Course from which to load the data.

    Returns
    -------
    dict
        A dictionary that contains the data.
    """
    filename = f'course_data/{course.id}-files.json'
    file_path = Path(filename)
    if not file_path.is_file():
        print(f'File data for {course.name} ({course.id}) not found at {filename}')
        print('Downloading data from Canvas')
        inventory(course.get_files(), filename)
    return json_read(filename)

def load_modules(course:Course) -> dict:
    """Loads the module data. First attempt is by file, then through Canvas.
	
    Parameters
    ----------
    course: Course
        The Course from which to load the data.

    Returns
    -------
    dict
        A dictionary that contains the data.
    """
    filename = f'course_data/{course.id}-modules.json'
    file_path = Path(filename)
    if not file_path.is_file():
        print(f'Module data for {course.name} ({course.id}) not found at {filename}')
        print('Downloading data from Canvas')
        inventory(course.get_modules(), filename)
    return json_read(filename)

def load_pages(course:Course) -> dict:
    """Loads the page data. First attempt is by file, then through Canvas.
	
    Parameters
    ----------
    course: Course
        The Course from which to load the data.

    Returns
    -------
    dict
        A dictionary that contains the data.
    """
    filename = f'course_data/{course.id}-pages.json'
    file_path = Path(filename)
    if not file_path.is_file():
        print(f'Page data for {course.name} ({course.id}) not found at {filename}')
        print('Downloading data from Canvas')
        inventory(course.get_pages(), filename, id='page_id')
    return json_read(filename)

def load_users(course:Course) -> dict:
    """Loads the page data. First attempt is by file, then through Canvas.
	
    Parameters
    ----------
    course: Course
        The Course from which to load the data.

    Returns
    -------
    dict
        A dictionary that contains the data.
    """
    filename = f'course_data/{course.id}-users.json'
    file_path = Path(filename)
    if not file_path.is_file():
        print(f'User data for {course.name} ({course.id}) not found at {filename}')
        print('Downloading data from Canvas')
        inventory(course.get_users(enrollment_type=['student', 'student_view', 'teacher', 'ta', 'designer', 'observer']), filename)
    return json_read(filename)

def paginated_to_dict(paginated: PaginatedList, id:str = 'id') -> dict:
    """Converts a PaginatedList into a dictionary of dictionaries whose keys are the indicated 
    key and whose contents are the Canvas objects. This process removes the datetime objects
    and requester object so that the data can be written to JSON without any problems.

    Parameters
    ----------
    paginated : PaginatedList
        The paginated list to be converted to a dictionary.
    id : str
        The key to use as the ID for the dictionary.

    Returns
    -------
    dict
        The dictionary containing the contents of paginated.
    """
    data = {}
    for object in paginated:
        data[object.__dict__[id]] = {
            key: item for key, item in object.__dict__.items()
            if key != '_requester' and not(key.endswith('_date'))
        }
    return data

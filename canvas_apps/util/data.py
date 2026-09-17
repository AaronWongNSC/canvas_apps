"""
Utilities to work with data
"""

from canvasapi.course import Course
from canvasapi.paginated_list import PaginatedList
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

def course_inventory(course:Course, folder:str = '') -> bool:
    """Creates a course inventory for the given course_id. The inventory includes
    modules, pages, assignments, assignment_groups, files, and users.

    Parameters
    ----------
    course_id : int
        The course_id of the course being inventoried

    Returns
    -------
    bool
        True if the inventory was successful. False if there was an error
    """
    try:
        if folder.endswith('/'):
            folder = folder[:-1]
        inventory(course.get_modules(), f'{folder}/{course.id}-modules.json')
        inventory(course.get_pages(), f'{folder}/{course.id}-pages.json', id='page_id')
        inventory(course.get_assignments(), f'{folder}/{course.id}-assignments.json')
        inventory(course.get_assignment_groups(), f'{folder}/{course.id}-assignment_groups.json')
        inventory(course.get_discussion_topics(), f'{folder}/{course.id}-discussion-topics.json')
        inventory(course.get_files(), f'{folder}/{course.id}-files.json')
        inventory(course.get_users(enrollment_type=['student', 'student_view', 'teacher']), f'{folder}/{course.id}-users.json')
        return True
    except:
        return False


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
            if target_value in contents[search_key]:
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
    try:
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'r') as in_file:
            return json.load(in_file)
    except:
        return {}

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

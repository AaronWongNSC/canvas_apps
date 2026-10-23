"""
Creates menus for different scenarios
"""
import csv

def display_message(message:str) -> None:
    """Standardized message system for short messages

    Parameters
    ----------
    message
        The message to display.
    
    Returns
    -------
    None
    """
    print(f'\n*** {message} ***\n')
    return 

def display_long_message(message_list:list[str]) -> None:
    """Standardized message system for long messages

    Parameters
    ----------
    message_list
        A list of strings to display
    
    Returns
    -------
    None
    """
    print(f'\n**********************************************************************')
    for message in message_list:
        print(f'** {message.strip()}')
    print(f'**********************************************************************')
    return 

def get_id_from_file(file:str = None) -> int:
    """Select an object from a list stored as a CSV file.

    Parameters
    ----------
    file
        A CSV file whose first row is 'id,name\n' and whose subsequent rows are the objects to select from.
        If omitted, the program will ask the user to enter the file name.

    Returns
    -------
    int
        The ID of the desired object.

    """
    if not file:
        filename = input(f'Enter the name of the file [default: {file}]: ')
        if filename == '':
            filename = file
    else:
        filename = file

    objects = []
    try:
        with open(filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            for index, row in enumerate(reader):
                print(f'{index}: {row['name']} ({row['id']})')
                objects.append(row['id'])

        if len(objects) > 0:
            choice = input('Select an object: ')
            return objects[int(choice)]
        else:
            print(f'No objects found in {filename}. Use the Course_List_Generator.exe program to reinitialize it.')
            return input('Enter ID: ')
    except:
        return False

def get_id_from_dict(object_dict:dict, name_key:str='name', id_key:str='id') -> int:
    """Select an object from a dict.

    Parameters
    ----------
    object_dict
        A dictionary of objects. The keys for object_dict can be anything.
    
    name_key
        The key for the name of the objects.
    
    id_key
        The key for the object ID.

    Returns
    -------
    int
        The ID of the desired object.

    """
    objects = []

    count = 0
    for key, object in object_dict.items():
        print(f'{count}: {object[name_key]} ({object[id_key]})')
        objects.append(object[id_key])
        count += 1

    if len(objects) > 0:
        choice = input('Select an object: ')
        return objects[int(choice)]
    else:
        print('No objects found')
        return input('Enter an object ID: ')

def get_ids_from_dict(object_dict:dict, name_key:str='name', id_key:str='id') -> list[int]:
    """Select multiple objects from a dict.

    Parameters
    ----------
    object_dict
        A dictionary of objects. The keys for object_dict can be anything.
    
    name_key
        The key for the name of the objects.
    
    id_key
        The key for the object ID.

    Returns
    -------
    list[int]
        A list of the IDs of the desired objects.

    """

    objects = [ object[id_key] for _, object in object_dict.items() ]

    if len(objects) > 0:
        choices = prompt(
            [ f'({count}) {object[name_key]} ({object[id_key]})' for count, (_, object) in enumerate(object_dict.items()) ],
            prompt='Selections (use commas to separate items):').split(',')
        return [ objects[int(choice)] for choice in choices ]
    else:
        print('No objects found')
        return input('Enter the object IDs (use a comma to separate items): ').split(',')


def get_id_from_list(object_list:list[dict], name_key:str='name', id_key:str='id') -> int:
    """Select an object from a list.

    Parameters
    ----------
    object_dict
        A dictionary of objects. The keys for object_dict can be anything.
    
    name_key
        The key for the name of the objects.
    
    id_key
        The key for the object ID.

    Returns
    -------
    int
        The ID of the desired object.
    """

    if len(object_list) > 0:
        selection = prompt([ f'{count}: {object[name_key]} ({object[id_key]})' for count, object in enumerate(object_list) ],
               title='COURSE SELECTION')
        return object_list[int(selection)][id_key]
    else:
        print('No objects found')
        return input('Enter an object ID: ')
   
def prompt(list_of_options:list[str], title:str = None, prompt:str = None, upper:bool = True) -> str:
    """Standardized menu display

    Parameters
    ----------
    list_of_options
        A list of strings that will represent the options.
    
    Returns
    -------
    str
        The selection (stripped and forced into uppercase)
    """
    if title == None:
        title = 'Select from the following list'
    if prompt == None:
        prompt = 'Selection:'

    print(f'\n--- {title} ---\n')
    for option in list_of_options:
        print(option)
    print()
    if upper:
        return input(prompt.strip() + ' ').strip().upper()
    return input(prompt.strip() + ' ').strip()

def sift_sort(object_dict:dict, search_key:str = None, sort_key:str = None) -> dict:
    """Search a dictionary for objects by one key and/or sort by another key.

    Parameters
    ----------
    object_dict
        A dictionary of objects.
    
    search_key
        The key for the text search.
    
    sort_key
        The key to sort by.

    Returns
    -------
    dict
        A dictionary with the sifted and/or sorted items

    """

    if search_key:
        search_string = input(f'Enter a search string for the object (key = {search_key}): ')
        object_dict = {
            id: object for id, object in object_dict.items()
                if search_string.upper() in object[search_key].upper()
        }

    if sort_key:
        object_dict = dict(sorted(object_dict.items(), key=lambda item: item[1][sort_key]))

    return object_dict
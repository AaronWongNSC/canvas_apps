"""
Creates menus for different scenarios
"""
import csv

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

        choice = input('Select an object: ')
        return objects[int(choice)]
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

    choice = input('Select an object: ')
    return objects[int(choice)]

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
                if search_string in object[search_key]
        }

    if sort_key:
        object_dict = dict(sorted(object_dict.items(), key=lambda item: item[1][sort_key]))

    return object_dict

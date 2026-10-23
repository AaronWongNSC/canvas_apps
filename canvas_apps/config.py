"""
Configuration Tools
"""

import json
from pathlib import Path
from datetime import datetime
from canvas_apps.ui import prompt


def load_config() -> dict:
    """Load the configuration file

    Parameters
    ----------
    None

    Returns
    -------
    dict
        The dictionary containing the configuration information
    """
    try:
        with open('config/config.json', 'r') as in_file:
            config = json.load(in_file)
    except:
        print('Configuration file not found at config/config.json. Creating a new configuration file.')
        folder_path = Path('config')
        folder_path.mkdir(parents=True, exist_ok=True)

        config = {
            'prefix': 'nevadastate',
            'main_key': {
                'key': None,
                'date': None
            },
            'beta_key': {
                'key': None,
                'date': None
            },
            'test_key': {
                'key': None,
                'date': None
            },
            'course_list': [],
        }
        save_config(config)
    return config

def save_config(config:dict) -> None:
    """Save the configuration file

    Parameters
    ----------
    config : dict
        The dictionary containing the configuration data

    Returns
    -------
    None
    """

    with open('config/config.json', 'w') as out_file:
        out_file.write(json.dumps(config, indent=4))
    return

def update_key(key_type:str):
    """Update API Key

    Parameters
    ----------
    key_type : str
        The key type is either 'main_key', 'beta_key', or 'test_key'.

    Returns
    -------
    None

    """
    def key_exists(key):
        if key['key']:
            return f'Stored on {key['date']}'
        return 'Missing'

    config = load_config()
    key = config[key_type]

    if key_type == 'main_key':
        url = ''
    else:
        url = key_type[:4] + '.'

    new_key = prompt([
        f'Key status: {key_exists(key)}\n',
        f'To get an API key:',
        f'1) Log into https://{config['prefix']}.{url}instructure.com',
        f'2) Click "Account" (at the top-left corner)',
        f'3) Select "Settings"',
        f'4) Click the blue "+ New Access Token" button',
        f'5) Enter a purpose (this can be anything), and an expiration date and time (typically a week or two in the future)',
        f'6) Click "Generate Token"',
        f'7) A window will pop up with your API key next to "Token" (it is the long string of text)',
        f'8) Copy and paste this below.',
        ],
        title=f'UPDATE {key_type[:4].upper()} KEY',
        prompt='Enter the new key (blank to keep the old one or CLEAR to delete):',
        upper=False)

    if not new_key: ## No change
        return key
    if new_key.upper() == 'CLEAR':
        config[key_type] = {
            'key': None,
            'date': None
        }
        save_config(config)
    else:
        config[key_type] = {
            'key': new_key,
            'date': datetime.now().strftime('%D')
        }
    save_config(config)
    return config[key_type]

import os
import os.path

import configparser
import distutils.util
import textwrap

CONFIG_FILE_NAME = ".remoterun"

DEFAULT_CONFIG_TEXT = textwrap.dedent('''
    # This is an initial remote run config
    # Set following options:

    # Url of host to sync
    RemoteHost = example.com

    # Path on the remote host to sync with
    RemoteDir = /home/foo/rr/
        
    # You can also select some optional arguments

    # Receive or not if remote command failed (yes/no/ask)
    # ReceiveIfFailed = ask
    ''').strip()

DEFAULTS = {
    'ReceiveIfFailed': 'ask',
    }


def find_config(directory):
    while True:
        config_file = os.path.join(directory, CONFIG_FILE_NAME)
        if os.path.exists(config_file):
            return config_file

        directory, splitted = os.path.split(directory)
        if not splitted:
            raise RuntimeError("RemoteRun not configured for this directory")


def parse_config(config_file):
    with open(config_file) as f:
        config_text = f.read()

    if config_text.find('[main]') == -1:
        config_text = '[main]\n' + config_text # Add placeholder section

    config_parser = configparser.ConfigParser(defaults=DEFAULTS)
    config_parser.read_string(config_text)

    return {
        'remote_host': config_parser['main']['RemoteHost'],
        'remote_root': config_parser['main']['RemoteDir'],
        'receive_if_failed': config_parser['main']['ReceiveIfFailed']
        }


def get_settings():
    local_dir = os.path.realpath(os.curdir)
    config_file = find_config(local_dir)
    local_root = os.path.dirname(config_file)

    settings = {
        'local_dir': local_dir,
        'local_root': local_root,
        'rel_path': os.path.relpath(local_dir, local_root)
        }

    settings.update(parse_config(config_file))
    settings['remote_dir'] = os.path.normpath(os.path.join(settings['remote_root'], settings['rel_path']))

    return settings


def create_initial_config():
    if os.path.exists(CONFIG_FILE_NAME):
        raise RuntimeError('Config is already saved in {}'.format(CONFIG_FILE_NAME)) 

    with open(CONFIG_FILE_NAME, mode='w') as config_file:
        print(DEFAULT_CONFIG_TEXT, file=config_file)

    os.system('vim {}'.format(CONFIG_FILE_NAME))



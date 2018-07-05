import os
import re

import yaml

CONFIG_FILE_ENV_VARIABLE = 'INSIDEAPP_CONFIG'


def get_file_path():
    path = '/etc/insideapp.yml'
    if CONFIG_FILE_ENV_VARIABLE in os.environ:
        env_path = os.environ[CONFIG_FILE_ENV_VARIABLE]
        path_regex = re.compile(r'\*.yml')
        if path_regex.match(env_path):
            path = env_path
    return path


def parse_config_file():
    path = get_file_path()
    with open(path, 'r') as stream:
        config = yaml.load(stream)
        return config

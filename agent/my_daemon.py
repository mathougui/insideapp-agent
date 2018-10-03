import logging
import os
from os.path import expanduser

import yaml

import main_loop
from daemon import Daemon

logger = logging.getLogger("insideapp-agent")
filename = f'{expanduser("~")}/.insideapp/insideapp.yml'


class MyDaemon(Daemon):

    def __init__(self, pidfile, args):
        super().__init__(pidfile)
        self.args = args

    def run(self):
        main_loop.main_loop(self.args)

    @staticmethod
    def status():
        try:
            with open(filename, 'r') as stream:
                config = yaml.load(stream)
                if not config:
                    config = {}
                print(config)
        except FileNotFoundError:
            logger.warning("No daemon configuration file found")

    @staticmethod
    def remove_config_file():
        os.remove(filename)

    @staticmethod
    def set_status(processes, api_key=None):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        try:
            with open(filename, 'w+') as stream:
                config = yaml.load(stream)
                if not config:
                    config = {}
                    if api_key:
                        config['api_key'] = api_key
                for process in processes:
                    config[process.process.name()] = process.process.ppid()
                yaml.dump(config, stream)
        except FileNotFoundError:
            logger.warning("No daemon configuration file found")

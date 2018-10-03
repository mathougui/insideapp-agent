import logging
import os
from os.path import expanduser

import yaml

import main_loop
from daemon import Daemon
from process import Process

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
                stream.truncate(0)
                config = {'api_key': api_key}
                for process in processes:
                    config[process.process.name()] = process.process.ppid()
                yaml.dump(config, stream)
        except FileNotFoundError:
            logger.warning("No daemon configuration file found")

    def update_processes(self, processes_name, processes_pid):
        processes = []
        if processes_name:
            for process_name in processes_name:
                processes.append(
                    Process.create_name_resource(process_name))
        if processes_pid:
            for resource_pid in processes_pid:
                processes.append(
                    Process.create_pid_resource(resource_pid))
        try:
            with open(filename, 'r+') as stream:
                config = yaml.load(stream)
            os.remove(filename)
            with open(filename, 'w+') as stream:
                new_config = {}
                try:
                    new_config = {'api_key': config['api_key']}
                except AttributeError:
                    pass
                for process in processes:
                    new_config[process.process.name()] = process.process.ppid()
                yaml.dump(new_config, stream)
        except FileNotFoundError:
            logger.warning("No daemon configuration file found")

import sys
import threading
import time

import requests
from requests.auth import HTTPBasicAuth

from logs import Log
from resources import Resources

import psutil


class MainLoop:
    resources = None
    resources_to_get = {'cpu_process': True, 'cpu_global': True, 'memory_process': True,
                        'memory_global': True, 'swap_process': True, 'swap_global': True}
    resources_functions = None
    logs_to_get         = {}
    api_key             = ""
    logs_url            = ""
    resources_url       = ""
    log                 = None

    def __init__(self):
        self.resources = Resources(sys.argv[2])
        self.api_key = sys.argv[1]
        self.log = Log(self.logs_to_get)
        self.resources_functions = {'cpu_process': self.resources.get_process_cpu_percent, 'cpu_global': self.resources.get_global_cpu_percent, 'memory_process': self.resources.get_process_memory_percent,
                                    'memory_global': self.resources.get_global_memory_percent, 'swap_process': self.resources.get_process_swap_percent, 'swap_global': self.resources.get_global_swap_percent}

    def launch_main_loop(self):
        self.get_resources_and_logs()

    def get_resources_and_logs(self):
        while True:
            if self.resources.process is not None:
                self.send_resources()
            self.send_logs()
            time.sleep(5)

    def send_resources(self):
        payload = self.get_all_needed_resources()
        self.make_request(payload, self.resources_url)

    def get_all_needed_resources(self):
        payload = {}
        try:
            with self.resources.process.oneshot():
                for p in self.resources_to_get:
                    resource = self.resources_functions[p]()
                    payload[p] = resource
        except psutil.NoSuchProcess:
            print('Could not find process "' + self.resources.process_name + '"')
        return payload

    def send_logs(self):
        payload = self.get_all_needed_logs()
        self.make_request(payload, self.logs_url)

    def get_all_needed_logs(self):
        payload = {}
        for log in self.logs_to_get:
            logs = self.log.get_logs(log)
            if logs:
                payload[log] = logs
        return payload

    def make_request(self, payload, url):
        if payload:
            pass
            # TODO Make Post request to API with basic auth

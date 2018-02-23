import sys
import threading
import time

import requests
from requests.auth import HTTPBasicAuth

from logs import Log
from resources import Resources


class MainLoop:
    resources = None
    resources_to_get = {'cpu_process': True, 'cpu_global': True, 'memory_process': True,
                        'memory_global': True, 'swap_process': True, 'swap_global': True}
    logs_to_get = {'nginx': '/var/log/nginx/error.log', 'apache': '/var/log/nginx/error.log.4'}
    api_key = ""
    logs_url = "http://insideapp.com/app/4564645456/logs"
    resources_url = "http://insideapp.com/app/4545665654/resources"
    log = None

    def __init__(self):
        self.resources = Resources(sys.argv[2])
        self.api_key = sys.argv[1]
        self.log = Log(self.logs_to_get)

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
        with self.resources.process.oneshot():
            if self.resources_to_get['cpu_process']:
                cpu_process = self.resources.get_process_cpu_percent()
                payload['cpu_process'] = cpu_process
            if self.resources_to_get['cpu_global']:
                cpu_global = self.resources.get_global_cpu_percent()
                payload['cpu_global'] = cpu_global
            if self.resources_to_get['memory_process']:
                memory_process = self.resources.get_process_memory_percent()
                payload['memory_process'] = memory_process
            if self.resources_to_get['memory_global']:
                memory_global = self.resources.get_global_memory_percent()
                payload['memory_global'] = memory_global
            if self.resources_to_get['swap_process']:
                swap_process = self.resources.get_process_swap_percent()
                payload['swap_process'] = swap_process
            if self.resources_to_get['swap_global']:
                swap_global = self.resources.get_global_swap_percent()
                payload['swap_global'] = swap_global
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
            requests.post(url, data=payload,
                          auth=HTTPBasicAuth('', self.api_key))

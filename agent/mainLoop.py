import sys
import threading
import time

import requests
from requests.auth import HTTPBasicAuth

from logs import get_logs
from resources import Resources


class MainLoop:
    resources = None
    resources_to_get = {'cpu_process': True, 'cpu_global': True, 'memory_process': True, 'memory_global': True, 'swap_process': True, 'swap_global': True}
    logs_to_get = {'nginx': '/var/log/nginx/error.log'}
    api_key = ""
    logs_url = "http://insideapp.com/app/4564645456/logs"
    resources_url = "http://insideapp.com/app/4545665654/resources"

    def __init__(self):
        self.resources = Resources(sys.argv[2])
        self.api_key = sys.argv[1]

    def make_request(self, payload, url):
        print(payload)
        requests.post(url, data=payload, auth=HTTPBasicAuth('', self.api_key))

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

    def get_all_needed_logs(self):
        payload = {}
        if self.logs_to_get['nginx']:
            logs = get_logs(self.logs_to_get['nginx'])
            payload['nginx'] = logs
        return payload

    def send_resources(self):
        payload = self.get_all_needed_resources()
        self.make_request(payload, self.resources_url)

    def send_logs(self):
        payload = self.get_all_needed_logs()
        print(payload)
        self.make_request(payload, self.logs_url)

    def get_resources_loop(self):
        while True:
            if self.resources.process is not None:
                self.send_resources()
                time.sleep(5)

    def launch_main_loop(self):
        threading.Thread(target=self.send_logs).start()
        threading.Thread(target=self.get_resources_loop).start()

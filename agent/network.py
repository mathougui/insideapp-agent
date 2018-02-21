import sys
import time

import requests

from resources import Resources


class ApiCall:
    resources = None
    resources_to_get = {'cpu_process': True, 'cpu_global': True, 'memory_process': True, 'memory_global': True, 'swap_process': True, 'swap_global': True}

    def __init__(self):
        self.resources = Resources(sys.argv[2])

    @staticmethod
    def make_request(payload):
        requests.post("http://insideapp.com/app/4ea5oe4a64ea/resources", data=payload)

    def fill_payload(self):
        payload = {'api_key': sys.argv[1]}
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
        print(payload)
        return payload

    def launch_main_loop(self):
        while True:
            if self.resources.process is not None:
                payload = self.fill_payload()
                self.make_request(payload)
                time.sleep(1)

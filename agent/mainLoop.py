import json
import sys
import time

import psutil
import requests
from requests.auth import HTTPBasicAuth

from logs import Log
from resources import Resources


class MainLoop:
    resources = None
    resources_to_get = {"CPU_app": True, "CPU_glob": True, "RAM_app": True,
                        "RAM_glob": True, "SWAP_app": True, "SWAP_glob": True}
    resources_functions = None
    logs_to_get = {"nginx": "/var/log/nginx/error.log"}
    api_key = ""
    logs_url = "http://localhost:3000/api/v1/logs"
    resources_url = "http://localhost:3000/api/v1/metrics"
    log = None

    def __init__(self):
        self.resources = Resources(sys.argv[2])
        self.api_key = sys.argv[1]
        self.log = Log(self.logs_to_get)
        self.resources_functions = {"CPU_app": self.resources.get_process_cpu_percent, "CPU_glob": self.resources.get_global_cpu_percent,
                                    "RAM_app": self.resources.get_process_memory_percent,
                                    "RAM_glob": self.resources.get_global_memory_percent, "SWAP_app": self.resources.get_process_swap_percent,
                                    "SWAP_glob": self.resources.get_global_swap_percent}

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
            print('Could not find process "' +
                  self.resources.process_name + '"')
        return payload

    def send_logs(self):
        payload = self.get_all_needed_logs()
        self.make_request(payload, self.logs_url)

    def get_all_needed_logs(self):
        payload = {"logs": []}
        for log in self.logs_to_get:
            logs = self.log.get_logs(log)
            if logs:
                log_data = {log: logs}
                payload["logs"] += [log_data]
        if not payload["logs"]:
            return {}
        return payload

    def make_request(self, payload, url):
        if payload:
            payload = json.dumps(payload)
            requests.post(url, data=payload,
                          auth=HTTPBasicAuth("", self.api_key))

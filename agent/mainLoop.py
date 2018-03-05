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
    resources_names = []
    resources_to_get = {}
    logs_to_get = {}
    logs_url = "http://localhost:3000/api/v1/logs"
    resources_url = "http://localhost:3000/api/v1/metrics"
    resources_functions = {}

    def fill_resources_to_get(self):
        for resource_name in self.resources_names:
            # TODO Get the real values from API
            self.resources_to_get[resource_name] = True

    def read_config_file(self):
        with open('config.json') as config_file:
            try:
                self.resources_names = json.load(config_file)["resources"]
                for resource in self.resources_names:
                    self.resources_functions[resource] = getattr(self.resources, "get_" + resource)
            except KeyError:
                exit(1)

    def __init__(self):
        self.resources = Resources(sys.argv[2])
        self.read_config_file()
        self.api_key = sys.argv[1]
        self.log = Log(self.logs_to_get)
        self.fill_resources_to_get()

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
                    try:
                        resource = self.resources_functions[p]()
                        payload[p] = resource
                    except IndexError:
                        pass
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

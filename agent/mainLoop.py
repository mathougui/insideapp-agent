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
    resources_names = ["cpu_time_user", "cpu_time_system", "cpu_time_idle", "cpu_percent", "cpu_freq_current", "ram_available", "ram_used", "ram_percent", "swap_used", "swap_free",
                       "swap_percent", "disk_used", "disk_free", "disk_percent", "disk_read_count", "disk_write_count", "disk_read_time", "disk_write_time", "network_bytes_sent",
                       "network_bytes_received", "network_packets_sent", "network_packets_received", "network_dropped_count_incoming", "network_dropped_count_outgoing",
                       "boot_time", "process_env_variables", "process_create_time", "process_status", "process_read_count", "process_write_count", "process_read_bytes",
                       "process_write_bytes", "process_cpu_percent", "process_swap_used", "process_swap_percent", "process_ram_used", "process_ram_percent"]
    resources_to_get = {}
    resources_functions = {}
    logs_to_get = {"nginx": "/var/log/nginx/error.log"}
    api_key = ""
    logs_url = "http://localhost:3000/api/v1/logs"
    resources_url = "http://localhost:3000/api/v1/metrics"
    log = None

    def fill_resources_to_get(self):
        for resource_name in self.resources_names:
            # TODO Get the real values from API
            self.resources_to_get[resource_name] = True

    def __init__(self):
        self.resources = Resources(sys.argv[2])
        self.api_key = sys.argv[1]
        self.log = Log(self.logs_to_get)
        self.resources_functions = {"CPU_app": self.resources.get_process_cpu_percent, "CPU_glob": self.resources.get_cpu_percent,
                                    "RAM_app": self.resources.get_process_ram_percent,
                                    "RAM_glob": self.resources.get_ram_percent, "SWAP_app": self.resources.get_process_swap_percent,
                                    "SWAP_glob": self.resources.get_swap_percent}
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

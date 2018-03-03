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
    logs_to_get = {"nginx": "/var/log/nginx/error.log"}
    logs_url = "http://localhost:3000/api/v1/logs"
    resources_url = "http://localhost:3000/api/v1/metrics"
    resources_functions = {}

    def fill_resources_to_get(self):
        for resource_name in self.resources_names:
            # TODO Get the real values from API
            self.resources_to_get[resource_name] = True

    def fill_resources_functions(self):
        self.resources_functions = {self.resources_names[0]: self.resources.get_cpu_time_user, self.resources_names[1]: self.resources.get_cpu_time_system,
                                    self.resources_names[2]: self.resources.get_cpu_time_idle, self.resources_names[3]: self.resources.get_cpu_percent,
                                    self.resources_names[4]: self.resources.get_cpu_freq_current, self.resources_names[5]: self.resources.get_ram_available,
                                    self.resources_names[6]: self.resources.get_ram_used, self.resources_names[7]: self.resources.get_ram_percent,
                                    self.resources_names[8]: self.resources.get_swap_used, self.resources_names[9]: self.resources.get_swap_free,
                                    self.resources_names[10]: self.resources.get_swap_percent, self.resources_names[11]: self.resources.get_disk_used,
                                    self.resources_names[12]: self.resources.get_disk_free, self.resources_names[13]: self.resources.get_disk_percent,
                                    self.resources_names[14]: self.resources.get_disk_read_count, self.resources_names[15]: self.resources.get_disk_write_count,
                                    self.resources_names[16]: self.resources.get_disk_read_time, self.resources_names[17]: self.resources.get_disk_write_time,
                                    self.resources_names[18]: self.resources.get_network_bytes_sent, self.resources_names[19]: self.resources.get_network_bytes_received,
                                    self.resources_names[20]: self.resources.get_network_packets_sent, self.resources_names[21]: self.resources.get_network_packets_received,
                                    self.resources_names[22]: self.resources.get_network_dropped_count_incoming,
                                    self.resources_names[23]: self.resources.get_network_dropped_count_outgoing, self.resources_names[24]: self.resources.get_boot_time,
                                    self.resources_names[25]: self.resources.get_process_env_variables, self.resources_names[26]: self.resources.get_process_create_time,
                                    self.resources_names[27]: self.resources.get_process_status, self.resources_names[28]: self.resources.get_process_read_count,
                                    self.resources_names[29]: self.resources.get_process_write_count, self.resources_names[30]: self.resources.get_process_read_bytes,
                                    self.resources_names[31]: self.resources.get_process_write_bytes, self.resources_names[32]: self.resources.get_process_cpu_percent,
                                    self.resources_names[33]: self.resources.get_process_swap_used, self.resources_names[34]: self.resources.get_process_swap_percent,
                                    self.resources_names[35]: self.resources.get_process_ram_used, self.resources_names[36]: self.resources.get_process_ram_percent}

    def __init__(self):
        self.resources = Resources(sys.argv[2])
        self.api_key = sys.argv[1]
        self.log = Log(self.logs_to_get)
        self.fill_resources_functions()
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
            print(payload)
            payload = json.dumps(payload)
            requests.post(url, data=payload,
                          auth=HTTPBasicAuth("", self.api_key))

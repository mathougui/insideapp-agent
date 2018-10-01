import json
import os
import sys
import time
import logging
import psutil
import urllib3
import requests
from requests.auth import HTTPBasicAuth
from threading import Thread
from logs import Log
from parse_config_file import parse_config_file

from process_list import ProcessList


class MainLoop:
    logger = logging.getLogger("insideapp-agent")

    def __init__(self, args):
        self.process_list = ProcessList(args.name, args.pid, args.api_key)
        # self.logs_to_get = parse_config_file()
        # self.log = Log(self.logs_to_get)

    def launch_main_loop(self):
        self.get_resources_and_logs()

    def get_resources_and_logs(self):
        while True:
            self.process_list.send_dynamic_resources_all_processes()
            # self.send_logs()
            time.sleep(5)

    """ def send_logs(self):
        payload = self.get_all_needed_logs()
        self.make_request(payload, self.logs_url)

    def get_all_needed_logs(self):
        payload = {"logs": []}
        if self.logs_to_get:
            for log in self.logs_to_get:
                logs = self.log.get_logs(log)
                if logs:
                    log_data = {"type": log, "messages": logs}
                    payload["logs"] += [log_data]
        if not payload["logs"]:
            return {}
        return payload """

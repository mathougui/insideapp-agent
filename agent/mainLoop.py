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

from process_list import ProcessList


class MainLoop:
    logger = logging.getLogger("insideapp-agent")

    def __init__(self, args):
        self.process_list = ProcessList(args.name, args.pid, args.api_key)
        self.logs = Log(args.api_key)

    def launch_main_loop(self):
        self.get_resources_and_logs()

    def get_resources_and_logs(self):
        while True:
            self.process_list.send_dynamic_resources_all_processes()
            self.logs.send_logs()
            time.sleep(5)

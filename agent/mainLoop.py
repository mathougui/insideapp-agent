import json
import os
import sys
import time
import logging
import psutil
import requests
from requests.auth import HTTPBasicAuth
from threading import Thread
from logs import Log
from parse_config_file import parse_config_file

from resources import Resources
from config import resources


class MainLoop:
    logger = logging.getLogger("insideapp-agent")
    resources = None
    dynamic_resources_names = []
    static_resources_names = []
    resources_to_get = []
    dynamic_resources_functions = {}
    static_resources_functions = {}
    api_url = "https://metrics.insideapp.io"
    admin_url = "https://insideapp.io/api/v1/configuration"
    logs_url = "https://logs.insideapp.io/api/v1/logs"
    dynamic_resources_url = api_url + "/api/v1/metrics/upload"
    static_resources_url = api_url + "/api/v1/metrics/static/upload"

    def fill_resources_to_get(self):
        for resource_name in self.dynamic_resources_names:
            self.resources_to_get += [resource_name]

    def read_config_file(self):
        try:
            self.dynamic_resources_names = resources["dynamic_resources"]
            self.static_resources_names = resources["static_resources"]
            for resource in self.dynamic_resources_names:
                self.dynamic_resources_functions[resource] = getattr(
                    self.resources, "get_" + resource)
            for resource in self.static_resources_names:
                self.static_resources_functions[resource] = getattr(
                    self.resources, "get_" + resource)
        except KeyError:
            sys.exit(1)

    def __init__(self, args):
        self.resources = Resources(name=args.name, pid=args.pid)
        self.read_config_file()
        self.logs_to_get = parse_config_file()
        self.api_key = args.api_key
        self.log = Log(self.logs_to_get)
        self.fill_resources_to_get()
        self.verbose = args.verbose
        if "API_URL" in os.environ:
            self.api_url = os.environ["API_URL"]
            self.dynamic_resources_url = self.api_url + "/api/v1/metrics/upload"
            self.static_resources_url = self.api_url + "/api/v1/metrics/static/upload"
            self.logs_url = self.api_url + "/api/v1/logs"
        if "ADMIN_URL" in os.environ:
            self.admin_url = os.environ["ADMIN_URL"] + "/api/v1/configuration"
        self.get_config()

    def get_config(self):
        r = requests.get(self.admin_url, auth=HTTPBasicAuth("", self.api_key))
        if not r or not r.json():
            self.logger.warning("Could not get configuration")
            sys.exit(1)
        else:
            config = r.json()
            if self.verbose:
                self.logger.debug("User configuration: " + str(config))
            self.resources_to_get = []
            for resource in config["resources"]:
                self.resources_to_get += [resource]
            for log in config["logs"]:
                self.logs_to_get[log["type"]] = log["path"]

    def get_config_loop(self):
        while True:
            self.get_config()
            time.sleep(30)

    def launch_main_loop(self):
        Thread(target=self.get_config_loop).start()
        self.send_static_resources()
        self.get_resources_and_logs()

    def send_static_resources(self):
        payload = {}
        try:
            for r in self.static_resources_names:
                try:
                    resource = self.static_resources_functions[r]()
                    payload[r] = resource
                except (IndexError, AttributeError):
                    pass
        except psutil.NoSuchProcess:
            self.logger.error('Could not find process "' +
                              self.resources.process + '"')
        if self.verbose:
            self.logger.info(self.static_resources_url +
                             ":\n\t" + str(payload))
        self.make_request(payload, self.static_resources_url)

    def get_resources_and_logs(self):
        while True:
            self.send_resources()
            self.send_logs()
            time.sleep(5)

    def send_resources(self):
        payload = self.get_all_needed_resources()
        self.make_request(payload, self.dynamic_resources_url)

    def get_all_needed_resources(self):
        payload = {}
        try:
            with self.resources.process.oneshot():
                for p in self.resources_to_get:
                    try:
                        resource = self.dynamic_resources_functions[p]()
                        payload[p] = resource
                    except IndexError:
                        pass
        except psutil.NoSuchProcess:
            self.logger.error(
                f"The process {self.resources.process.name} is no longer available")
            sys.exit(1)
        except AttributeError:
            # No process has been specified
            for p in self.resources_to_get:
                try:
                    resource = self.dynamic_resources_functions[p]()
                    payload[p] = resource
                except IndexError:
                    pass
                except AttributeError:
                    self.logger.error(f"{p}: To get this resource, you must specify a process to monitor")
        return payload

    def send_logs(self):
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
        return payload

    def make_request(self, payload, url):
        payload["timestamp"] = round(time.time() * 1000)
        payload = json.dumps(payload)
        self.logger.debug(url + ":\n\t" + payload)
        try:
            requests.post(url, data=payload,
                          auth=HTTPBasicAuth("", self.api_key), verify=False)
        except Exception as e:
            self.logger.error(
                f"Could not connect to {url}: {e}")

import urllib3
import requests
import sys
import logging
import os
import time
import json

from requests.auth import HTTPBasicAuth


class Network():
    api_key = None

    logger = logging.getLogger("insideapp-agent")

    admin_url = "https://insideapp.io/api/v1/configuration"
    metrics_url = "https://metrics.insideapp.io"
    logs_url = "https://logs.insideapp.io/api/v1/logs"

    def get_dynamic_resources_url(self):
        return self.metrics_url + "/api/v1/metrics/upload"

    def get_static_resources_url(self):
        return self.metrics_url + "/api/v1/metrics/static/upload"

    def __init__(self, api_key):
        self.api_key = api_key
        self.get_env_variables()

        urllib3.disable_warnings()

    def get_env_variables(self):
        if "METRICS_URL" in os.environ:
            self.metrics_url = os.environ["METRICS_URL"]
        if "LOGS_URL" in os.environ:
            self.logs_url = os.environ["LOGS_URL"]
        if "ADMIN_URL" in os.environ:
            self.admin_url = os.environ["ADMIN_URL"] + "/api/v1/configuration"

    def get_resources_configuration(self):
        resources_to_get = []
        self.logger.debug("toto")
        r = requests.get(self.admin_url, auth=HTTPBasicAuth("", self.api_key))
        if not r or not r.json():
            self.logger.warning(
                f'Could not get configuration from {self.admin_url}, please try again later')
            sys.exit(1)
        else:
            config = r.json()
            self.logger.debug("User configuration: " + str(config))
            for resource in config["resources"]:
                resources_to_get += [resource]
        return resources_to_get

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

    def send_static_resources(self, payload):
        self.make_request(payload, self.get_static_resources_url())

    def send_dynamic_resources(self, payload):
        self.make_request(payload, self.get_dynamic_resources_url())
    
    def send_logs(self, payload):
        self.make_request(payload, self.logs_url)

import logging
import sys

import psutil

import my_daemon
from config import resources
from network import Network
from process import Process


class ProcessList:
    processes = []
    static_resources_names = []
    dynamic_resources_names = []
    dynamic_resources_functions = {}
    static_resources_functions = {}
    resources_to_get = []
    logs_to_get = []
    network = None

    logger = logging.getLogger("insideapp-agent")

    def __init__(self, processes_name, processes_pid, api_key):
        self.network = Network(api_key)

        if processes_name:
            for process_name in processes_name:
                self.processes.append(
                    Process.create_name_resource(process_name))
        if processes_pid:
            for resource_pid in processes_pid:
                self.processes.append(
                    Process.create_pid_resource(resource_pid))

        my_daemon.MyDaemon.set_status(self.processes, api_key=api_key)

        if len(self.processes) == 0:
            self.processes.append(Process(None))

        self.create_resources_methods_name_dict()

    def get_resources_configuration(self):
        self.resources_to_get = self.network.get_resources_configuration()

    def create_resources_methods_name_dict(self):
        try:
            self.dynamic_resources_names = resources["dynamic_resources"]
            self.static_resources_names = resources["static_resources"]
            for process in self.processes:
                for resource in self.dynamic_resources_names:
                    self.dynamic_resources_functions[resource] = getattr(
                        process, "get_" + resource)
            for resource in self.static_resources_names:
                self.static_resources_functions[resource] = getattr(
                    self.processes[0], "get_" + resource)
        except KeyError:
            sys.exit(1)
        except IndexError:
            pass

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
            self.logger.error(
                'An error occured while fetching static resources. Please try again.')
            sys.exit(1)
        self.network.send_static_resources(payload)

    def send_dynamic_resources_all_processes(self):
        payload = {}
        if not self.processes:
            payload = self.send_dynamic_resources(None)
        for process in self.processes:
            payload = self.send_dynamic_resources(process)
        self.network.send_dynamic_resources(payload)

    def send_dynamic_resources(self, process):
        payload = {}
        try:
            with process.process.oneshot():
                for p in self.resources_to_get:
                    try:
                        r = self.dynamic_resources_functions[p]()
                        payload[p] = r
                    except IndexError:
                        pass
        except psutil.NoSuchProcess:
            self.logger.error(
                f"The process {process.name} is no longer available")
            sys.exit(1)
        except AttributeError:
            # No process has been specified
            for resource in self.resources_to_get:
                try:
                    r = self.dynamic_resources_functions[resource]()
                    payload[resource] = r
                except IndexError:
                    pass
                except AttributeError:
                    self.logger.error(
                        f'{resource}: to monitor this resource, you must specify a process to monitor')
        return payload

    def update_processes(self, pids):
        self.processes = [Process.create_pid_resource(pid) for pid in pids]

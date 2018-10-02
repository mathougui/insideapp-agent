import sys

from network import Network
from parse_config_file import parse_config_file


class Log:
    files = {}
    filenames = []

    def __init__(self, api_key):
        self.filenames = parse_config_file()
        self.network = Network(api_key)
        self.open_files()

    def open_files(self):
        if self.filenames:
            for filename in self.filenames:
                try:
                    file = open(self.filenames[filename], 'r')
                    file.seek(0, 2)
                    self.files[filename] = file
                except FileNotFoundError:
                    print("Could not find file: " + self.filenames[filename])
                    sys.exit(1)

    def send_logs(self):
        payload = self.get_all_logs()
        self.network.send_logs(payload)

    def get_all_logs(self):
        payload = {"logs": []}
        if self.filenames:
            for log in self.filenames:
                logs = self.get_logs(log)
                if logs:
                    log_data = {"type": log, "messages": logs}
                    payload["logs"] += [log_data]
        if not payload["logs"]:
            return {}
        return payload

    def get_logs(self, log_type):
        lines = self.files[log_type].readlines()
        to_remove = []
        for index, line in enumerate(lines):
            striped_line = line.rstrip('\n')
            if not striped_line:
                to_remove += line
            else:
                lines[index] = striped_line
        for element in to_remove:
            lines.remove(element)
        return lines

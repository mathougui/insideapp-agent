import time

from logs import Log
from process_list import ProcessList


def main_loop(args):
    process_list = ProcessList(args.name, args.pid, args.api_key)
    logs = Log(args.api_key)
    while True:
        process_list.get_resources_configuration()
        process_list.send_dynamic_resources_all_processes()
        logs.send_logs()
        time.sleep(5)

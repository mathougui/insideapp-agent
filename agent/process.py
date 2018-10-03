import datetime
import logging
import sys
import time

import psutil


def to_mb(nb_bytes):
    return nb_bytes / 1048576


def format_date(date):
    tz = str(time.timezone // 3600)
    if tz[0] != '-' or tz[0] == '+':
        tz = "+" + tz
    if len(tz) < 3:
        tz = tz[0] + "0" + tz[1]
    tz = date + tz + ":00"
    return tz


class Process:
    process = None

    def __init__(self, process):
        self.process = process

    @staticmethod
    def create_name_resource(resource_name):
        logger = logging.getLogger("insideapp-agent")
        possible_processes = []
        # Get all the processes with the specified name
        for p in psutil.process_iter(attrs=['name']):
            if p.info['name'] == resource_name:
                possible_processes.append(p)
        # If no process with this name was found, exit
        if len(possible_processes) == 0:
            logger.error(
                f'Could not find a process with name {resource_name}')
            sys.exit(1)
        # If more than one process with this name was found, exit
        if len(possible_processes) > 1:
            logger.error(
                'Multiple processes have this name, please specify a pid instead')
            sys.exit(1)
        return Process(possible_processes[0])

    @staticmethod
    def create_pid_resource(resource_pid):
        logger = logging.getLogger("insideapp-agent")
        try:
            return Process(psutil.Process(int(resource_pid)))
        except psutil._exceptions.NoSuchProcess:
            logger.error(
                f"Could not find a process with pid {resource_pid}")
            sys.exit(1)
        except ValueError:
            logger.error(f"PID {resource_pid} must be an integer")
            sys.exit(1)

    @staticmethod
    def get_cpu_time_user():
        return psutil.cpu_times()[0]

    @staticmethod
    def get_cpu_time_system():
        return psutil.cpu_times()[2]

    @staticmethod
    def get_cpu_time_idle():
        return psutil.cpu_times()[3]

    @staticmethod
    def get_cpu_percent():
        return psutil.cpu_percent()

    @staticmethod
    def get_cpu_freq_current():
        return psutil.cpu_freq()[0]

    @staticmethod
    def get_ram_available():
        return to_mb(psutil.virtual_memory()[1])

    @staticmethod
    def get_ram_used():
        return to_mb(psutil.virtual_memory()[3])

    @staticmethod
    def get_ram_percent():
        return psutil.virtual_memory()[2]

    @staticmethod
    def get_swap_used():
        return to_mb(psutil.swap_memory()[1])

    @staticmethod
    def get_swap_free():
        return to_mb(psutil.swap_memory()[2])

    @staticmethod
    def get_swap_percent():
        return psutil.swap_memory()[3]

    @staticmethod
    def get_disk_used():
        return to_mb(psutil.disk_usage("/")[1])

    @staticmethod
    def get_disk_free():
        return to_mb(psutil.disk_usage("/")[2])

    @staticmethod
    def get_disk_percent():
        return psutil.disk_usage('/')[3]

    @staticmethod
    def get_disk_read_count():
        return psutil.disk_io_counters()[0]

    @staticmethod
    def get_disk_write_count():
        return psutil.disk_io_counters()[1]

    @staticmethod
    def get_disk_read_time():
        return psutil.disk_io_counters()[2]

    @staticmethod
    def get_disk_write_time():
        return psutil.disk_io_counters()[3]

    @staticmethod
    def get_network_bytes_sent():
        return to_mb(psutil.net_io_counters()[0])

    @staticmethod
    def get_network_bytes_received():
        return to_mb(psutil.net_io_counters()[1])

    @staticmethod
    def get_network_packets_sent():
        return psutil.net_io_counters()[2]

    @staticmethod
    def get_network_packets_received():
        return psutil.net_io_counters()[3]

    @staticmethod
    def get_network_dropped_count_incoming():
        return psutil.net_io_counters()[6]

    @staticmethod
    def get_network_dropped_count_outgoing():
        return psutil.net_io_counters()[7]

    @staticmethod
    def get_boot_time():
        return format_date(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%dT%H:%M:%S"))

    @staticmethod
    def get_ram_total():
        return to_mb(psutil.virtual_memory()[0])

    @staticmethod
    def get_swap_total():
        return to_mb(psutil.swap_memory()[0])

    def get_process_create_time(self):
        return format_date(datetime.datetime.fromtimestamp(self.process.create_time()).strftime("%Y-%m-%dT%H:%M:%S"))

    def get_process_read_count(self):
        return self.process.io_counters()[0]

    def get_process_write_count(self):
        return self.process.io_counters()[1]

    def get_process_read_bytes(self):
        return self.process.io_counters()[2]

    def get_process_write_bytes(self):
        return self.process.io_counters()[3]

    def get_process_cpu_percent(self):
        return self.process.cpu_percent()

    def get_process_swap_used(self):
        return to_mb(self.process.memory_full_info()[9])

    def get_process_swap_percent(self):
        try:
            return (self.process.memory_full_info()[9]) * 100 / psutil.swap_memory()[0]
        except ZeroDivisionError:
            return 0

    def get_process_ram_used(self):
        return to_mb(self.process.memory_full_info()[0])

    def get_process_ram_percent(self):
        return self.process.memory_percent()

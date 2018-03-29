import datetime

import psutil


def to_mb(nb_bytes):
    return nb_bytes / 1048576


class Resources:
    process_name = ""
    process = None
    psutil_status_to_string = {psutil.STATUS_RUNNING: "Running", psutil.STATUS_DEAD: "Dead", psutil.STATUS_DISK_SLEEP: "Disk Sleep", psutil.STATUS_IDLE: "Idle",
                               psutil.STATUS_LOCKED: "Locked", psutil.STATUS_SLEEPING: "Sleeping", psutil.STATUS_STOPPED: "Stopped", psutil.STATUS_TRACING_STOP: "Tracing stop",
                               psutil.STATUS_WAITING: "Waiting", psutil.STATUS_WAKING: "Waking", psutil.STATUS_ZOMBIE: "Zombie"}

    def __init__(self, process_name):
        self.process_name = process_name
        self.search_for_process()

    def search_for_process(self):
        list_processes = []
        for p in psutil.process_iter(attrs=['name']):
            if self.process_name in p.info['name']:
                list_processes.append(p)
        if len(list_processes) > 0:
            self.process = list_processes[0]
        else:
            print('Could not find process "' + self.process_name + '"')
            exit(1)

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
        return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_ram_total():
        return to_mb(psutil.virtual_memory()[0])

    @staticmethod
    def get_swap_total():
        return to_mb(psutil.swap_memory()[0])

    def get_process_env_variables(self):
        return self.process.environ()

    def get_process_create_time(self):
        return datetime.datetime.fromtimestamp(self.process.create_time()).strftime("%Y-%m-%d %H:%M:%S")

    def get_process_status(self):
        return self.psutil_status_to_string[self.process.status()]

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

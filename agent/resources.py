import psutil


class Resources:
    process_name = ""
    process = None

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

    def get_process_cpu_percent(self):
        return self.process.cpu_percent()

    @staticmethod
    def get_global_cpu_percent():
        return psutil.cpu_percent()

    def get_process_memory_percent(self):
        return self.process.memory_percent()

    @staticmethod
    def get_global_memory_percent():
        try:
            return psutil.virtual_memory()[2]
        except IndexError:
            print("Could not load global RAM info")

    def get_process_swap_percent(self):
        try:
            return (self.process.memory_full_info()[9]) * 100 / psutil.swap_memory()[0]
        except IndexError:
            print("Could not load process SWAP info")

    @staticmethod
    def get_global_swap_percent():
        try:
            return psutil.swap_memory()[3]
        except IndexError:
            print("Could not load global SWAP info")

    @staticmethod
    def get_global_disk_usage_percent():
        try:
            # TODO partitions?
            # TODO check if "/" works on windows
            return psutil.disk_usage('/')[3] / 1000000
        except IndexError:
            print("Could not load global disk usage info")

    @staticmethod
    def get_total_memory():
        try:
            return psutil.virtual_memory()[0] / 1000000000
        except IndexError:
            print("Could not load total RAM info")

    @staticmethod
    def get_total_swap():
        try:
            return psutil.swap_memory()[0] / 1000000000
        except IndexError:
            print("Could not load total SWAP info")

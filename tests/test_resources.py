import unittest

from agent import process_list

class ResourceTest(unittest.TestCase):
    process_list = process_list.ProcessList(processes_name=["python3.6"], processes_pid=None, api_key="")

    def test_cpu_time_user(self):
        self.assertGreater(self.process_list.processes[0].get_cpu_time_user(), 0)

    def test_cpu_time_system(self):
        self.assertGreater(self.process_list.processes[0].get_cpu_time_system(), 0)

    def test_cpu_time_idle(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_cpu_time_idle(), 0)

    def test_cpu_percent(self):
        percent = self.process_list.processes[0].get_cpu_percent()
        self.assertGreaterEqual(percent, 0)
        self.assertLessEqual(percent, 100)

    def test_ram_available(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_ram_available(), 0)

    def test_ram_used(self):
        self.assertGreater(self.process_list.processes[0].get_ram_used(), 0)

    def test_ram_percent(self):
        percent = self.process_list.processes[0].get_ram_percent()
        self.assertGreaterEqual(percent, 0)
        self.assertLessEqual(percent, 100)

    def test_swap_used(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_swap_used(), 0)

    def test_swap_free(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_swap_free(), 0)

    def test_swap_percent(self):
        percent = self.process_list.processes[0].get_swap_percent()
        self.assertGreaterEqual(percent, 0)
        self.assertLessEqual(percent, 100)

    def test_disk_used(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_disk_used(), 0)

    def test_disk_free(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_disk_free(), 0)

    def test_disk_percent(self):
        percent = self.process_list.processes[0].get_disk_percent()
        self.assertGreaterEqual(percent, 0)
        self.assertLessEqual(percent, 100)

    def test_disk_read_count(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_disk_read_count(), 0)

    def test_disk_write_count(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_disk_write_count(), 0)

    def test_disk_read_time(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_disk_read_time(), 0)

    def test_network_bytes_sent(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_network_bytes_sent(), 0)

    def test_network_bytes_received(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_network_bytes_received(), 0)

    def test_network_packets_sent(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_network_packets_sent(), 0)

    def test_network_packets_received(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_network_packets_received(), 0)

    def test_network_dropped_count_incoming(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_network_dropped_count_incoming(), 0)

    def test_network_dropped_count_outgoing(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_network_dropped_count_outgoing(), 0)

    def test_ram_total(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_ram_total(), 0)

    def test_swap_total(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_swap_total(), 0)

    def test_process_read_count(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_process_read_count(), 0)

    def test_process_write_count(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_process_write_count(), 0)

    def test_process_read_bytes(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_process_read_bytes(), 0)

    def test_process_write_bytes(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_process_write_bytes(), 0)

    def test_process_cpu_percent(self):
        percent = self.process_list.processes[0].get_process_cpu_percent()
        self.assertGreaterEqual(percent, 0)
        self.assertLessEqual(percent, 100)

    def test_process_swap_used(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_process_swap_used(), 0)

    def test_process_swap_percent(self):
        percent = self.process_list.processes[0].get_process_swap_percent()
        self.assertGreaterEqual(percent, 0)
        self.assertLessEqual(percent, 100)

    def test_process_ram_used(self):
        self.assertGreaterEqual(self.process_list.processes[0].get_process_ram_used(), 0)

    def test_process_ram_percent(self):
        percent = self.process_list.processes[0].get_process_ram_percent()
        self.assertGreaterEqual(percent, 0)
        self.assertLessEqual(percent, 100)

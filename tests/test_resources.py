import unittest

from agent import resources


class ResourceTest(unittest.TestCase):
    resource = resources.Resources("pytest")

    def test_cpu_time_user(self):
        self.assertGreater(self.resource.get_cpu_time_user(), 0)

    def test_cpu_time_system(self):
        self.assertGreater(self.resource.get_cpu_time_system(), 0)

    def test_cpu_time_idle(self):
        self.assertGreaterEqual(self.resource.get_cpu_time_idle(), 0)

    def test_cpu_percent(self):
        self.assertGreaterEqual(self.resource.get_cpu_percent(), 0)
        self.assertLessEqual(self.resource.get_cpu_percent(), 100)

    def test_ram_available(self):
        self.assertGreaterEqual(self.resource.get_ram_available(), 0)

    def test_ram_used(self):
        self.assertGreater(self.resource.get_ram_used(), 0)

    def test_ram_percent(self):
        self.assertGreaterEqual(self.resource.get_ram_percent(), 0)
        self.assertLessEqual(self.resource.get_ram_percent(), 100)

    def test_swap_used(self):
        self.assertGreaterEqual(self.resource.get_swap_used(), 0)

    def test_swap_free(self):
        self.assertGreaterEqual(self.resource.get_swap_free(), 0)

    def test_swap_percent(self):
        self.assertGreaterEqual(self.resource.get_swap_percent(), 0)
        self.assertLessEqual(self.resource.get_swap_percent(), 100)

    def test_disk_used(self):
        self.assertGreaterEqual(self.resource.get_disk_used(), 0)

    def test_disk_free(self):
        self.assertGreaterEqual(self.resource.get_disk_free(), 0)

    def test_disk_percent(self):
        self.assertGreaterEqual(self.resource.get_disk_percent(), 0)
        self.assertLessEqual(self.resource.get_disk_percent(), 100)

    def test_disk_read_count(self):
        self.assertGreaterEqual(self.resource.get_disk_read_count(), 0)

    def test_disk_write_count(self):
        self.assertGreaterEqual(self.resource.get_disk_write_count(), 0)

    def test_disk_read_time(self):
        self.assertGreaterEqual(self.resource.get_disk_read_time(), 0)

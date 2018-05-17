import os
import unittest

from agent import logs


def write_to_file(to_write, single_line):
    file = open("tests/test_file.txt", "w+")
    log = logs.Log({"TestLog": "tests/test_file.txt"})
    if single_line:
        file.write(to_write)
    else:
        file.writelines(to_write)
    file.flush()
    received = log.get_logs("TestLog")
    os.remove("tests/test_file.txt")
    return received


class LogTest(unittest.TestCase):

    def test_write_log_one_line(self):
        received = write_to_file("Hello World!", single_line=True)
        self.assertEqual(received, ["Hello World!"])

    def test_write_log_multiple_lines(self):
        received = write_to_file(["Hello World!\n", "Goodbye World!"], single_line=False)
        self.assertEqual(received, ["Hello World!", "Goodbye World!"])

    def test_write_log_multiple_lines_with_empty_lines(self):
        received = write_to_file(["Hello World!\n", "\n", "Goodbye World!", "\n"], single_line=False)
        self.assertEqual(received, ["Hello World!", "Goodbye World!"])

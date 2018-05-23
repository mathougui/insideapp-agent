import argparse
import os
import signal
import sys

from mainLoop import MainLoop


def signal_handler(sig, frame):
    os.kill(os.getpid(), signal.SIGINT)
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('api_key', action="store")
    parser.add_argument('process_name', action="store")
    args = parser.parse_args()

    main_loop = MainLoop(args)
    main_loop.launch_main_loop()


if __name__ == "__main__":
    main()

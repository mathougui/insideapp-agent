import argparse
import os
import signal
import sys
import platform
import logging

from daemon import Daemon
from mainLoop import MainLoop


class MyDaemon(Daemon):

    def __init__(self, pidfile, args):
        super().__init__(pidfile)
        self.args = args

    def run(self):
        launch_main_loop(self.args)


def signal_handler(sig, frame):
    os.kill(os.getpid(), signal.SIGINT)
    sys.exit(0)


def launch_main_loop(args):
    main_loop = MainLoop(args)
    main_loop.launch_main_loop()


def setup_logger(verbose):
    logger = logging.getLogger("insideapp-agent")
    logger.setLevel(logging.DEBUG)

    # Setup file logging.
    log_filename = '/var/log/insideapp/insideapp-agent.log'
    if not os.path.exists(os.path.dirname(log_filename)):
        os.makedirs(os.path.dirname(log_filename))
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)
    fhFormatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s')
    fh.setFormatter(fhFormatter)
    logger.addHandler(fh)

    # Setup console logging
    ch = logging.StreamHandler()
    if verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)
    chFormatter = logging.Formatter(
        '%(levelname)s - %(message)s')
    ch.setFormatter(chFormatter)
    logger.addHandler(ch)

    return logger


def main():
    # Configure Signal Handler
    signal.signal(signal.SIGINT, signal_handler)

    first_arg = sys.argv[1]
    if (first_arg == "start" or first_arg == "stop") and platform.system() != "Windows":
        del sys.argv[1]
        if first_arg == "stop":
            daemon = MyDaemon('insideapp_pid', [])
            daemon.stop()
            exit(0)

    # Configure ArgumentParser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('-p', '--pid', action="store")
    parser.add_argument('-n', '--name', action="store")
    parser.add_argument('--api_key', action="store")
    args = parser.parse_args()

    # Check root privileges
    if os.getuid() != 0:
        print("Please launch the agent with root privileges")
        exit(1)

    # Setup logger
    logger = setup_logger(args.verbose)

    if not args.api_key:
        logger.error("You must provide an API key")
        exit(1)

    if first_arg == "start" and platform.system() != "Windows":
        # Setup Daemon
        daemon = MyDaemon('insideapp_pid', args)
        daemon.start()
    else:
        # Launch in foreground
        launch_main_loop(args)


if __name__ == "__main__":
    main()

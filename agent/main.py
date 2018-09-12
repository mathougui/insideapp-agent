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


def setup_logger(verbose=False):
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


def check_api_key(args, logger):
    if not args.api_key:
        logger.error("You must provide an API key")
        sys.exit(1)


def add_optional_arguments_to_parser(parser):
    parser.add_argument('-v', '--verbose', action="store_true", help="Enable verbose logs (What ressources are sent to the server, etc)")
    parser.add_argument('-p', '--pid', action="store", help="Specify the pid of the process to monitor")
    parser.add_argument('-n', '--name', action="store", help="Specify the name of the process to monitor")
    parser.add_argument('--api_key', action="store", help='Specify the api key for your application (you can find it at "https://insideapp.io/apps/<your_app>/settings")')


def main():
    # Configure Signal Handler
    signal.signal(signal.SIGINT, signal_handler)

    # Configure ArgumentParser
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest="command")

    start_parser = subparser.add_parser("start", help="Start the agent in foreground mode")
    add_optional_arguments_to_parser(start_parser)

    daemon_parser = subparser.add_parser("daemon", help="Access the daemon commands (start and stop)")
    daemon_subparser = daemon_parser.add_subparsers(dest="daemon")

    daemon_start_parser = daemon_subparser.add_parser("start", help="Start the agent in daemon mode")
    add_optional_arguments_to_parser(daemon_start_parser)

    daemon_subparser.add_parser("stop", help="Stop the agent if it was ran in daemon mode")

    args = parser.parse_args()

    # Check root privileges
    if os.getuid() != 0:
        print("Please launch the agent with root privileges")
        sys.exit(1)

    # Setup logger
    try:
        logger = setup_logger(args.verbose)
    except AttributeError:
        # Args.verbose is not defined (because the program was launched with the daemon stop command, etc...)
        logger = setup_logger()

    if args.command == "daemon" and platform.system() != "Windows":
        # Setup Daemon
        daemon = MyDaemon('insideapp_pid', args)
        if args.daemon == "start":
            check_api_key(args, logger)
            daemon.start()
        elif args.daemon == "stop":
            daemon.stop()
    else:
        # Launch in foreground
        check_api_key(args, logger)
        launch_main_loop(args)


if __name__ == "__main__":
    main()

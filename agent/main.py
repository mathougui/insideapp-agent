import os
import platform
import signal
import sys

import parser
from logger import create_logger
from main_loop import main_loop
from my_daemon import MyDaemon


# noinspection PyUnusedLocal
def signal_handler(sig, frame):
    os.kill(os.getpid(), signal.SIGINT)
    sys.exit(0)


def check_api_key(args, logger):
    if not args.api_key:
        logger.error("You must provide an API key")
        sys.exit(1)


def check_root_privileges():
    if os.getuid() != 0:
        print("Please launch the agent with root privileges")
        sys.exit(1)


def launch_main_loop(args, logger):
    daemon = MyDaemon('insideapp_pid', args)
    if args.command == "stop":
        daemon.stop()
        MyDaemon.remove_config_file()
    elif args.command == "status":
        daemon.status()
    elif not args.verbose and platform.system() != "Windows" and args.command == "start":
        # Setup Daemon
        check_api_key(args, logger)
        daemon.start()
    else:
        # Launch in foreground
        check_api_key(args, logger)
        main_loop(args)


def main():
    # Configure Signal Handler
    signal.signal(signal.SIGINT, signal_handler)

    # Configure ArgumentParser
    args = parser.parse_arguments()

    # Check root privileges
    check_root_privileges()

    # Setup logger
    logger = create_logger(args)

    # Get and send logs and resources to the server every few seconds
    launch_main_loop(args, logger)


if __name__ == "__main__":
    main()

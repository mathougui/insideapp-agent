import argparse
import os
import signal
import sys

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


def main():
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('-p', '--pid', action="store")
    parser.add_argument('-n', '--name', action="store")
    parser.add_argument('api_key', action="store")
    args = parser.parse_args()

    if not args.verbose:
        daemon = MyDaemon('insideapp_pid', args)
        if sys.argv[1] == 'stop':
            daemon.stop()
        else:
            daemon.start()
    else:
        launch_main_loop(args)


if __name__ == "__main__":
    main()

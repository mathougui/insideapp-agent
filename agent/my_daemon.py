from daemon import Daemon
from main_loop import main_loop


class MyDaemon(Daemon):

    def __init__(self, pidfile, args):
        super().__init__(pidfile)
        self.args = args

    def run(self):
        main_loop(self.args)

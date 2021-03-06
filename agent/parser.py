import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest="command")

    start_parser = subparser.add_parser(
        "start", help="Start the agent in foreground mode")
    add_optional_arguments_to_parser(start_parser)

    subparser.add_parser(
        "stop", help="Stop the agent if it was ran in daemon mode")

    subparser.add_parser(
        "status", help="Show the current configuration of the agent"
    )

    update_parser = subparser.add_parser(
        "update", help="Update the processes to monitor"
    )
    update_parser.add_argument('-p', '--pid', action="store",
                               help="Specify the pid of the process to monitor", nargs='+')
    update_parser.add_argument('-n', '--name', action="store",
                               help="Specify the name of the process to monitor", nargs='+')

    return parser.parse_args()


def add_optional_arguments_to_parser(parser):
    parser.add_argument('-v', '--verbose', action="store_true",
                        help="Enable verbose logs (What ressources are sent to the server, etc)")
    parser.add_argument('-p', '--pid', action="store",
                        help="Specify the pid of the process to monitor", nargs='+')
    parser.add_argument('-n', '--name', action="store",
                        help="Specify the name of the process to monitor", nargs='+')
    parser.add_argument('--api_key', action="store",
                        help='Specify the api key for your application (you can find it at "https://insideapp.io/apps/<your_app>/settings")')

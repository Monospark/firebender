import argparse
import os
import subprocess
import sys

import dragon_link
import json_parser
import logging
from firebender import loader
from server import Server, DragonServer, WsrServer, Status


def main():
    parser = argparse.ArgumentParser(add_help=True, description="Control firebender")
    subparsers = parser.add_subparsers(help="commands")
    start_group = subparsers.add_parser("start")
    start_group.add_argument("engine", action="store", choices=("dragon", "wsr"))
    start_group.add_argument("-s", "--shell", action="store_true")
    start_group.add_argument("-l", "--locale", action="store", default="en")
    start_group.add_argument("-m", "--modules", action="store", default=None)
    start_group.add_argument("-c", "--configs", action="store", default=None)

    stop_group = subparsers.add_parser("stop")

    status_group = subparsers.add_parser("status")

    link_group = subparsers.add_parser("dragon")
    link_group.add_argument("action", action="store", choices=("link", "unlink"))

    args = parser.parse_args()

    if "status" in sys.argv:
        print Server.get_status_string()
        return 0

    if "dragon" == sys.argv[1]:
        if args.action == "link":
            dragon_link.install()
        else:
            dragon_link.uninstall()
        return

    if "stop" in sys.argv:
        Server.send_stop()
        return 0

    if not args.shell:
        modified_arguments = list(sys.argv[1:])
        modified_arguments.insert(0, "firebender")
        modified_arguments.append("-s")
        subprocess.Popen(" ".join(modified_arguments))
        return 0

    if Server.get_status() != Status.INACTIVE:
        print "Server is already running"
        return 1

    if args.modules is None:
        print("Missing modules parameter")
        return 1
    if not os.path.isdir(args.modules):
        print("modules parameter is not an existing directory")
        return 1
    if args.configs is None:
        print("Missing configs parameter")
        return 1
    if not os.path.isdir(args.configs):
        print("configs parameter is not an existing directory")
        return 1
    loader.modules_directory = args.modules
    loader.configs_directory = args.configs
    loader.locale = args.locale

    logging.basicConfig(level=logging.INFO)
    if args.engine == "dragon":
        data = json_parser.parse_json("dragon_data.json")
        if data is None:
            print("Run firebender dragon link first.")
            return 1

        DragonServer(data["location"])
    else:
        WsrServer()


if __name__ == '__main__':
    main()

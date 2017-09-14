import argparse
import subprocess
import sys

import dragon_link
from server import Server, DragonServer, WsrServer, Status


def main():
    parser = argparse.ArgumentParser(add_help=True, description="Control dragonfly_loader")
    subparsers = parser.add_subparsers(help="commands")
    start_group = subparsers.add_parser("start")
    start_group.add_argument("engine", action="store", choices=("dragon", "wsr"))
    start_group.add_argument("-s", "--shell", action="store_true")

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

    if "stop" in sys.argv:
        Server.send_stop()
        return 0

    if not args.shell:
        modified_arguments = list(sys.argv[1:])
        modified_arguments.insert(0, "dragonfly_loader")
        modified_arguments.append("-s")
        subprocess.Popen(" ".join(modified_arguments))
        return 0

    if Server.get_status() != Status.INACTIVE:
        print "Server is already running"
        return 1

    if args.engine == "dragon":
        DragonServer()
    else:
        WsrServer()


if __name__ == '__main__':
    main()

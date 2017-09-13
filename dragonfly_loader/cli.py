import argparse
import subprocess
import sys

from server import Server, DragonServer, WsrServer


def main():
    parser = argparse.ArgumentParser(add_help=True, description="Control dragonfly_loader")
    subparsers = parser.add_subparsers(help="commands")
    start_group = subparsers.add_parser("start")
    start_group.add_argument("engine", action="store", choices=("dragon", "wsr"))
    start_group.add_argument("-s", "--shell", action="store_true")

    stop_group = subparsers.add_parser("stop")

    status_group = subparsers.add_parser("status")

    args = parser.parse_args()

    if "status" in sys.argv:
        print Server.get_status_string()
        return

    if "stop" in sys.argv:
        Server.send_stop()
        return

    if not args.shell:
        modified_arguments = list(sys.argv[1:])
        modified_arguments.insert(0, "dragonfly_loader")
        modified_arguments.append("-s")
        subprocess.Popen(" ".join(modified_arguments))
        return

    if args.engine == "dragon":
        DragonServer()
    else:
        WsrServer()


if __name__ == '__main__':
    main()

import argparse

import logging
import subprocess

import sys

import instance
import loader
import pythoncom
import time

from dragonfly.engines.backend_sapi5.engine import Sapi5InProcEngine

import server


def main():
    parser = argparse.ArgumentParser(add_help=True, description="Control dragonfly_loader")
    subparsers = parser.add_subparsers(help="commands")
    start_group = subparsers.add_parser("start")
    start_group.add_argument("engine", action="store", choices=("dragon", "wsr"))
    start_group.add_argument("-l", "--log", action="store_true")
    start_group.add_argument("-s", "--shell", action="store_true")

    stop_group = subparsers.add_parser("stop")
    stop_group.add_argument("-f", "--force", action="store_true")

    status_group = subparsers.add_parser("status")

    args = parser.parse_args()
    if args.shell:
        modified_arguments = list(sys.argv)
        modified_arguments.append("-s")
        subprocess.Popen(" ".join(modified_arguments))
        return

    if "status" in sys.argv:
        print server.DragonServer.get_status_string()
        return

    if "stop" is sys.argv:
        server.Server.stop_server()

    if args.engine == "dragon":
        server.DragonServer()
    else:
        server.WsrServer()


def start_wsr():

    logging.basicConfig(level=logging.INFO)
    engine = Sapi5InProcEngine()
    engine.connect()

    loader.start(loader.WSR)

    engine.speak('beginning loop!')
    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.1)
    wsr_connector.destroy()


if __name__ == '__main__':
    main()

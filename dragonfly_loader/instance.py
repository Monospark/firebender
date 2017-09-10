
import logging
import subprocess
from win32process import DETACHED_PROCESS

import loader
import pythoncom
import time

import signal
from dragonfly.engines.backend_sapi5.engine import Sapi5InProcEngine


__instance = None


def start(engine, shell, log):
    global __instance
    __instance = WsrInstance() if engine == loader.WSR else DragonInstance()
    __instance.start(shell, log)


def stop():
    __instance.stop(False)


class Instance:
    def __init__(self):
        pass

    def start(self, shell, log):
        pass

    def stop(self, force):
        pass


class WsrInstance(Instance):
    def __init__(self):
        Instance.__init__(self)
        self.__running = True

    def start(self, shell, log):
        logging.basicConfig(level=logging.INFO)
        engine = Sapi5InProcEngine()
        engine.connect()

        loader.start(loader.WSR)

        engine.speak('beginning loop!')
        while self.__running:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)

    def stop(self, force):
        self.__running = False
        time.sleep(0.1)
        loader.shutdown()


class DragonInstance(Instance):
    def __init__(self):
        Instance.__init__(self)
        self.__process = None

    def stop(self, force):
        self.__process.send_signal(signal.SIGTERM)

    def start(self, shell, log):
        path = "E:\\Program Files (x86)\\Nuance\\NaturallySpeaking13\\Program\\natspeak.exe"
        self.__process = subprocess.Popen([path], creationflags=DETACHED_PROCESS)

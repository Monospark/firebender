import time
import logging
import pythoncom
import loader

from dragonfly.engines.backend_sapi5.engine import Sapi5InProcEngine

__is_running = True


def quit():
    global __is_running
    __is_running = False


def init():
    logging.basicConfig(level=logging.INFO)
    engine = Sapi5InProcEngine()
    engine.connect()

    loader.start(loader.WSR)

    engine.speak('beginning loop!')


def destroy():
    loader.shutdown()


def loop():
    pythoncom.PumpWaitingMessages()
    time.sleep(0.1)
    global __is_running
    return __is_running

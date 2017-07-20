import time
import logging
import pythoncom
import dragonfly_loader

from dragonfly.engines.backend_sapi5.engine import Sapi5InProcEngine


running = True


def quit():
    global running
    running = False


def __main():
    logging.basicConfig(level=logging.INFO)
    engine = Sapi5InProcEngine()
    engine.connect()

    dragonfly_loader.start(dragonfly_loader.WSR)

    engine.speak('beginning loop!')
    while running:
        pythoncom.PumpWaitingMessages()
        time.sleep(.1)

    dragonfly_loader.shutdown()

if __name__ == "__main__":
    __main()

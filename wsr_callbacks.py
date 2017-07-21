from threading import Thread
import time
import dragonfly.timer


class __CallbackThread(Thread):
    def __init__(self, callbacks):
        Thread.__init__(self)
        self.__callbacks = callbacks
        self.__running = True

    def run(self):
        while self.__running:
            for callback in self.__callbacks:
                now = time.clock()
                if callback.next_time < now:
                    callback.call()
            time.sleep(0.025)

    def stop(self):
        self.__running = False

__thread = None


def init_callbacks(callbacks):
    callback_objects = [dragonfly.timer._Timer.Callback(c[0], c[1]) for c in callbacks]

    global __thread
    __thread = __CallbackThread(callback_objects)
    __thread.start()


def destroy_callbacks():
    __thread.stop()

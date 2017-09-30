import natlink
import time
from threading import Thread

import loader


class Callback(object):
    def __init__(self, function, interval):
        self.function = function
        self.interval = interval
        self.next_time = time.clock() + self.interval

    def call(self):
        self.next_time += self.interval
        try:
            self.function()
        except Exception, e:
            print "Exception during timer callback: %s (%r)" % (e, e)


INTERVAL = 0.025


class CallbackImplementation:
    def __init__(self):
        pass

    def initialize(self, callbacks):
        pass

    def destroy(self):
        pass


class WsrCallbacks(CallbackImplementation):
    class __CallbackThread(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.__callbacks = None
            self.__running = True

        def start_callbacks(self, callbacks):
            self.__callbacks = callbacks
            self.start()

        def run(self):
            while self.__running:
                for callback in self.__callbacks:
                    now = time.clock()
                    if callback.next_time < now:
                        callback.call()
                time.sleep(INTERVAL)

        def stop(self):
            self.__running = False

    def __init__(self):
        CallbackImplementation.__init__(self)
        self.__thread = WsrCallbacks.__CallbackThread()

    def initialize(self, callbacks):
        self.__thread.start_callbacks(callbacks)

    def destroy(self):
        self.__thread.stop()


class NatlinkCallbacks(CallbackImplementation):
    def __init__(self):
        CallbackImplementation.__init__(self)
        self.__callbacks = None

    def __natlink_callback(self):
        now = time.clock()
        for c in self.__callbacks:
            if c.next_time < now: c.call()

    def initialize(self, callbacks):
        if callbacks:
            self.__callbacks = callbacks
            #natlink.setTimerCallback(self.__natlink_callback, int(INTERVAL * 1000))

    def destroy(self):
        if self.__callbacks:
            pass
            #natlink.setTimerCallback(self.__natlink_callback, 0)


__impl = None


def init_callbacks(callbacks):
    callback_objects = [Callback(c[0], c[1]) for c in callbacks]

    global __impl
    if loader.get_engine_type() == loader.NATLINK:
        __impl = NatlinkCallbacks()
    else:
        __impl = WsrCallbacks()

    __impl.initialize(callback_objects)


def destroy_callbacks():
    global __impl
    __impl.destroy()

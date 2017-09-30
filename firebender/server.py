import logging
import socket
import subprocess
import sys
import threading
import time
from multiprocessing import connection
from multiprocessing.connection import Listener, Client
from win32process import DETACHED_PROCESS

import dragonfire
import psutil
import pythoncom

from firebender import loader

TIMEOUT = 0.5
connection._init_timeout = lambda: time.time() + TIMEOUT
ADDRESS = ('localhost', 6001)


class Action:
    ACK = 1
    STOP = 2
    GET_STATUS = 3
    SET_STATUS = 4
    GET_ENGINE = 5
    WRITE_OUTPUT = 6
    WRITE_ERROR = 7


class EngineType:
    DRAGON = 1
    WSR = 2

    _names = {
        DRAGON: "Dragon",
        WSR: "WSR"
    }

    @staticmethod
    def get_string(type):
        return EngineType._names[type]


class Status:
    STARTING_ENGINE = 1
    LOADING_MODULES = 2
    RUNNING = 3
    UNLOADING_MODULES = 4
    STOPPING_ENGINE = 5
    INACTIVE = 6

    _messages = {
        STARTING_ENGINE: "Starting engine",
        LOADING_MODULES: "Loading modules",
        RUNNING: "Running",
        UNLOADING_MODULES: "Unloading modules",
        STOPPING_ENGINE: "Stopping engine",
        INACTIVE: "Inactive"
    }

    @staticmethod
    def get_message(status):
        return Status._messages[status]


class Server:
    @staticmethod
    def communicate(data):
        conn = Client(ADDRESS)
        conn.send(data)
        received = conn.recv()
        return received

    @staticmethod
    def send_stop():
        Server.communicate(Action.STOP)

    @staticmethod
    def write_output(string):
        try:
            Server.communicate((Action.WRITE_OUTPUT, string))
        except socket.error:
            pass

    @staticmethod
    def write_error(string):
        try:
            Server.communicate((Action.WRITE_ERROR, string))
        except socket.error:
            pass

    @staticmethod
    def get_status():
        try:
            return Server.communicate(Action.GET_STATUS)
        except socket.error:
            return Status.INACTIVE

    @staticmethod
    def get_status_string():
        status = Server.get_status()
        if status == Status.INACTIVE:
            return Status.get_message(status)
        else:
            return Status.get_message(status) + " - " + EngineType.get_string(Server.communicate(Action.GET_ENGINE))

    @staticmethod
    def set_status(status):
        Server.communicate((Action.SET_STATUS, status))

    def __init__(self, type):
        self.__type = type
        self._status = Status.INACTIVE
        self.start_server()
        self.listener = Listener(ADDRESS)
        self.listener._listener._socket.settimeout(TIMEOUT)
        self.loop()

    def start_server(self):
        pass

    def stop_server(self):
        pass

    def is_active(self):
        pass

    def loop(self):
        while self.is_active():
            try:
                conn = self.listener.accept()
            except socket.timeout:
                continue
            except socket.error:
                break
            else:
                self.handle_connection(conn)
        self.listener.close()

    def stop(self):
        self.stop_server()

    def handle_connection(self, conn):
        msg = conn.recv()
        action_answer = self.handle_action(msg)
        if action_answer is not None:
            conn.send(action_answer)
        else:
            data_answer = self.handle_data(msg)
            if data_answer:
                conn.send(data_answer)

    def handle_action(self, message):
        if message == Action.STOP:
            self.stop()
            return Action.ACK
        if message == Action.GET_STATUS:
            return self._status
        if message == Action.GET_ENGINE:
            return self.__type
        return None

    def handle_data(self, message):
        action, data = message
        if action == Action.SET_STATUS:
            self._status = data
            return Action.ACK
        if action == Action.WRITE_OUTPUT:
            sys.stdout.write(data)
            return Action.ACK
        if action == Action.WRITE_ERROR:
            sys.stderr.write(data)
            return Action.ACK
        return None


class DragonServer(Server):
    def __init__(self, location):
        self.__location = location
        Server.__init__(self, EngineType.DRAGON)

    def start_server(self):
        dragonfire.engines.start_server()
        popen = subprocess.Popen([self.__location], creationflags=DETACHED_PROCESS)
        self.__process = psutil.Process(popen.pid)
        self._status = Status.STARTING_ENGINE

    def handle_data(self, message):
        action, data = message
        if action == Action.SET_STATUS:
            if data == Status.LOADING_MODULES:
                loader.load(loader.NATLINK)
        return Server.handle_data(self, message)

    def is_active(self):
        return self.__process.is_running()

    def stop_server(self):
        def terminate_or_kill():
            if not self.__process.is_running():
                return

            self._status = Status.STOPPING_ENGINE
            self.__process.kill()
            time.sleep(5)
            if self.__process.is_running():
                self.__process.terminate()

        threading.Thread(target=terminate_or_kill).start()


class WsrServer(Server):
    def __init__(self):
        self.__running = True
        Server.__init__(self, EngineType.WSR)

    def start_server(self):
        self._status = Status.STARTING_ENGINE
        logging.basicConfig(level=logging.INFO)
        engine = Sapi5InProcEngine()
        engine.connect()

        self._status = Status.LOADING_MODULES
        loader.start(loader.WSR)

        self._status = Status.RUNNING
        engine.speak('beginning loop!')
        threading.Thread(target=self.update).start()

    def update(self):
        while self.__running:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)

    def is_active(self):
        return self.__running

    def stop_server(self):
        self.__running = False
        self._status = Status.UNLOADING_MODULES
        loader.shutdown()

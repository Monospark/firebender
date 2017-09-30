import natlink

from server import Server, Status, DragonServer
from dragonfly.engines import get_engine

should_load = Server.get_status() == Status.STARTING_ENGINE
if should_load:
    Server.set_status(Status.LOADING_MODULES)
    Server.set_status(Status.RUNNING)
    get_engine()


def unload():
    pass

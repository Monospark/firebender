from dragonfire.engines import get_engine

from server import Server, Status

should_load = Server.get_status() == Status.STARTING_ENGINE
if should_load:
    Server.set_status(Status.LOADING_MODULES)
    Server.set_status(Status.RUNNING)
    get_engine()


def unload():
    pass

import loader
from server import Server, Status

should_load = Server.get_status() != Status.INACTIVE
if not should_load:
    raise loader.error
else:
    Server.set_status(Status.LOADING_MODULES)
    loader.start(loader.NATLINK)

Server.set_status(Status.RUNNING)


def unload():
    if should_load:
        Server.set_status(Status.UNLOADING_MODULES)
        loader.shutdown()

    Server.set_status(Status.STOPPING_ENGINE)


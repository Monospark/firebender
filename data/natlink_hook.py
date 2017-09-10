import loader
from server import DragonServer

DragonServer.natlink_load()

should_load = DragonServer.get_status() != DragonServer.Status.INACTIVE
if should_load:
    DragonServer.set_status(DragonServer.Status.LOADING_MODULES)
    loader.start(loader.NATLINK)

DragonServer.set_status(DragonServer.Status.RUNNING)


def unload():
    if should_load:
        DragonServer.set_status(DragonServer.Status.UNLOADING_MODULES)
        loader.shutdown()

    DragonServer.set_status(DragonServer.Status.STOPPING_DRAGON)


import dragonfly_loader

dragonfly_loader.start(dragonfly_loader.NATLINK)


def unload():
    dragonfly_loader.shutdown()

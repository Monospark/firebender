import loader

loader.start(loader.NATLINK)


def unload():
    loader.shutdown()

import dragonfly_loader


class Unit:

    def __init__(self, grammar_name=None, engine_types=[dragonfly_loader.NATLINK, dragonfly_loader.WSR]):
        self.__grammar_name = grammar_name
        self.__engine_types = engine_types

    @property
    def grammar_name(self):
        return self.__grammar_name

    @property
    def engine_types(self):
        return self.__engine_types

    def init(self):
        pass

    def destroy(self):
        pass

    def load_data(self, data):
        pass

    def save_data(self):
        pass

    def load_config(self, config_path):
        pass

    def create_grammar(self, g, t):
        pass

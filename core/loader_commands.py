from dragonfly import *
from unit import Unit
import dragonfly_loader


class LoaderCommands(Unit):
    def __init__(self):
        Unit.__init__(self, "loader_commands")
        self.__loaded_grammars = DictList("g")
        self.__loaded_grammars_ref = DictListRef("g", self.__loaded_grammars)

    def init(self):
        self.__loaded_grammars.update(dragonfly_loader.get_grammars())

    def __enable_grammar(g):
        if g.enabled:
            print("Grammar %s is already enabled" % g.name)
        else:
            g.enable()
            print("Grammar %s enabled" % g.name)

    def __disable_grammar(g):
        if not g.enabled:
            print("Grammar %s is not enabled" % g.name)
        else:
            g.disable()
            print("Grammar %s disabled" % g.name)

    def __reload_data(self):
        engine_type = dragonfly_loader.engine_type
        enabled_grammar_names = [name for name, g in self.__loaded_grammars.iteritems() if g.enabled]

        data = dragonfly_loader.save_module_data()
        dragonfly_loader.shutdown()
        dragonfly_loader.start(engine_type)
        dragonfly_loader.load_module_data(data)

        for grammar_name in enabled_grammar_names:
            if self.__loaded_grammars.has_key(grammar_name):
                g = self.__loaded_grammars[grammar_name]
                if not g.enabled:
                    self.__enable_grammar(g)

    def create_grammar(self, g, t):
        rule = MappingRule(
            mapping={
                t("reload_modules"): Function(lambda: self.__reload_data()),
                t("enable_grammar"): Function(lambda: self.__enable_grammar()),
                t("disable_grammar"): Function(lambda: self.__disable_grammar())
            },
            extras=[self.__loaded_grammars_ref]
        )
        g.add_rule(rule)
        return True


def create_unit():
    return LoaderCommands()

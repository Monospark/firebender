from dragonfly import *
from unit import Unit
import wsr_starter
import dragonfly_loader


class WsrCommands(Unit):
    def __init__(self):
        Unit.__init__(self, "wsr_commands", [dragonfly_loader.WSR])

    def create_grammar(self, g, t):
        rule = MappingRule(
            mapping={
                t("quit"): Function(wsr_starter.quit)
            }
        )
        g.add_rule(rule)
        return True

    def load_config(self, config_path):
        pass


def create_unit():
    return WsrCommands()

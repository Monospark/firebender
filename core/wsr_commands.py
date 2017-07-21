from dragonfly import *
from unit import Unit
import dragonfly_loader
import wsr_connector


class WsrCommands(Unit):
    def __init__(self):
        Unit.__init__(self, "wsr_commands", [dragonfly_loader.WSR])
        self.__paused = False
        self.__disabled_grammars = None

    def stop_listening(self):
        if not self.__paused:
            self.__paused = True
        else:
            return

        enabled_grammars = [g for g in dragonfly_loader.get_grammars() if g.enabled]
        for grammar in enabled_grammars:
            grammar.disable()
        self.__disabled_grammars = enabled_grammars

    def wake_up(self):
        if self.__paused:
            self.__paused = False
        else:
            return

        for grammar in self.__disabled_grammars:
            grammar.enable()
        self.__disabled_grammars = None

    def create_grammar(self, g, t):
        rule = MappingRule(
            mapping={
                t("quit"): Function(wsr_connector.quit),
                t("stop_listening"): Function(lambda: self.stop_listening()),
                t("wake_up"): Function(lambda: self.wake_up())
            }
        )
        g.add_rule(rule)
        return True

    def load_config(self, config_path):
        pass


def create_unit():
    return WsrCommands()

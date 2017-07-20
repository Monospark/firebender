from dragonfly import *
from unit import Unit


class ExampleUnit(Unit):
    def __init__(self):
        Unit.__init__(self, "example_grammar")

    def init(self):
        Unit.init(self)

    def create_grammar(self, g, t):
        rule = MappingRule(
            mapping={
                t("example_string"): Text("Hi")
            }
        )
        g.add_rule(rule)
        return True

    def load_config(self, config_path):
        pass

def create_unit():
    return ExampleUnit()

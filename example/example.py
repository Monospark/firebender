import dragonfly.timer
from dragonfly import *
from unit import Unit


class ExampleUnit(Unit):
    def __init__(self):
        Unit.__init__(self, "example_grammar")

    def init(self):
        pass

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

    def some_callback(self):
        print "This gets executed every second"

    def create_callbacks(self):
        return [(lambda: self.some_callback(), 1)]

def create_unit():
    return ExampleUnit()

import sys
import os
import pkgutil
import imp
import traceback
from dragonfly import *

# Load config.py
import config
root_path = os.path.dirname(os.path.abspath(__file__))
absolute_modules_directory = config.modules_dir
if not os.path.isabs(config.modules_dir):
    absolute_modules_directory = os.path.join(root_path, config.modules_dir)
absolute_config_dir = config.config_dir
if not os.path.isabs(config.config_dir):
    absolute_config_dir = os.path.join(root_path, config.config_dir)

absolute_excluded_files = [os.path.join(absolute_modules_directory, e) for e in config.excluded]


loaded_modules = []
loaded_grammars = DictList("g")
loaded_grammars_ref = DictListRef("g", loaded_grammars)

sys.argv = ["name"]


def __load_package(path):
    if path in absolute_excluded_files:
        return

    package_name = os.path.basename(path)
    package_dotted_name = os.path.normpath(path).replace(os.path.sep, ".")
    package_tuple = imp.find_module(package_name, [os.path.dirname(path)])
    package = imp.load_module(package_dotted_name, *package_tuple)

    loaded_modules.append(package)
    print(" - pkg %s" % package_dotted_name)

    prefix = package_dotted_name + "."
    for importer, module_name, ispkg in pkgutil.iter_modules([package_tuple[1]], prefix):
        module_path = os.path.join(path, module_name)
        if module_path in absolute_excluded_files:
            continue
        elif ispkg:
            __load_package(os.path.join(path, module_name))
        elif module_name in sys.modules:
            module = sys.modules[module_name]
            loaded_modules.append(module)
            print(" - (%s)" % module_name)
        else:
            try:
                module = importer.find_module(module_name).load_module(module_name)
                loaded_modules.append(module)
            except:
                print("Could not load %s:" % module_name)
                print(traceback.format_exc())
                continue
            else:
                print(" - %s" % module_name)


def __load_modules():
    print("\nLoading modules:")
    __load_package(absolute_modules_directory)

    print("\nInitializing modules:")
    __call_functions("load")


def __unload_modules():
    print("\nUnloading modules:")
    __call_functions("unload")

    print("\nDeleting modules:")
    for module in list(loaded_modules):
        loaded_modules.remove(module)
        del sys.modules[module.__name__]
        print(" - %s" % module.__name__)
        del module


def __save_module_data():
    data = {}
    print("\nSaving module data:")
    for module in __get_modules_with_function("save_data"):
        data[module.__name__] = __call_function(module, "save_data")
    return data


def __load_module_data(data):
    print("\nLoading module data:")
    for module in __get_modules_with_function("load_data"):
        __call_function(module, "load_data", data=data[module.__name__])


def __load_grammars():
    print("\nLoading grammars:")
    for module in __get_modules_with_function("create_grammar"):
        loaded_grammar, enabled = __call_function(module, "create_grammar")
        loaded_grammar.load()
        if not enabled:
            loaded_grammar.disable()
        loaded_grammars[loaded_grammar.name] = loaded_grammar
        print(" - %s" % loaded_grammar.name)


def __unload_grammars():
    print("\nUnloading grammars:")
    for g in loaded_grammars.values():
        print(" - %s" % g.name)
        g.unload()
    loaded_grammars.clear()


def __get_modules_with_function(name):
    return [m for m in loaded_modules if name in m.__dict__]


def __call_function(module, name, **kwargs):
    if name in module.__dict__:
        try:
            function = getattr(module, name)
            returned = function(**kwargs)
            print(" - %s" % module.__name__)
            return returned
        except:
            print("Could not call function %s of %s:" % (name, module.__name__))
            print(traceback.format_exc())


def __call_functions(name, **kwargs):
    for module in loaded_modules:
        __call_function(module, name, **kwargs)


def __load_configurations():
    print("\nLoading configurations:")
    __call_functions("load_config", config_path=absolute_config_dir)


def __create_reload_command():

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

    def __reload_data():
        enabled_grammar_names = [name for name, g in loaded_grammars.iteritems() if g.enabled]
        data = __save_module_data()

        __unload_grammars()
        __unload_modules()
        __load_modules()
        __load_configurations()
        __load_grammars()
        __load_module_data(data)

        for grammar_name in enabled_grammar_names:
            if loaded_grammars.has_key(grammar_name):
                g = loaded_grammars[grammar_name]
                if not g.enabled:
                    __enable_grammar(g)

    rule = MappingRule(
        mapping={
            "reload modules": Function(__reload_data),
            "enable <g> grammar": Function(__enable_grammar),
            "disable <g> grammar": Function(__disable_grammar),
        },
        extras=[loaded_grammars_ref]
    )

    grammar = Grammar("dragonfly loader")
    grammar.add_rule(rule)
    grammar.load()


__load_modules()
__load_configurations()
__load_grammars()
__create_reload_command()


def unload():
    __unload_grammars()
    __unload_modules()

    global grammar
    if grammar:
        grammar.unload()
    grammar = None

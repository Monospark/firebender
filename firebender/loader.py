import imp
import os
import pkgutil
import sys
import traceback

import i18n
from dragonfire import *

import callbacks

__loaded_modules = {}
__grammars = []

NATLINK = 0
WSR = 1
__engine_type = None
locale = None
modules_directory = None
configs_directory = None


def __get_units():
    return [u for u in __loaded_modules.values() if u is not None]


def __get_module_by_unit(unit):
    for m, u in __loaded_modules.iteritems():
        if u is unit:
            return m
    return None


def __call_function(unit, name, output=True, **kwargs):
    try:
        function = getattr(unit, name)
        returned = function(**kwargs)
        if output:
            print(" - %s" % unit.name)
        return returned
    except:
        print("Could not call function %s of %s:" % (name, unit))
        print(traceback.format_exc())


def __add_module(m):
    unit = None
    if "create_unit" in m.__dict__:
        u = m.create_unit()
        if __engine_type in u.engine_types:
            unit = u
    __loaded_modules[m] = unit


def __load_package(path, package_name):
    package_tuple = imp.find_module(os.path.basename(path), [os.path.dirname(path)])
    package = imp.load_module(package_name, *package_tuple)
    __loaded_modules[package] = None
    prefix = package_name + "."
    for importer, module_name, ispkg in pkgutil.iter_modules([package_tuple[1]], prefix):
        module_path = os.path.join(path, module_name[len(prefix):])
        if ispkg:
            __load_package(module_path, module_name)
        elif module_name in sys.modules:
            module = sys.modules[module_name]
            __add_module(module)
            print(" - (%s)" % module_name)
        else:
            try:
                module = importer.find_module(module_name).load_module(module_name)
                __add_module(module)
            except:
                print("Could not load %s:" % module_name)
                print(traceback.format_exc())
                continue
            else:
                print(" - %s" % module_name)


def __load_modules():
    print("\nLoading modules:")
    directories = [os.path.join(modules_directory, f) for f in os.listdir(modules_directory)]
    packages = [f for f in directories if os.path.isdir(f)]
    sys.path.append(modules_directory)

    for package in packages:
        __load_package(package, os.path.basename(package))

    print("\nInitializing units:")
    for unit in __get_units():
        __call_function(unit, "init")


def __unload_modules():
    print("\nDestroying units:")
    for unit in __get_units():
        __call_function(unit, "destroy")

    print("\nDeleting modules:")
    for module in __loaded_modules.keys():
        del __loaded_modules[module]
        del sys.modules[module.__name__]
        print(" - %s" % module.__name__)
        del module


def __create_callbacks():
    print("\nCreating callbacks:")
    callback_list = []
    for unit in __get_units():
        callback_list.extend(__call_function(unit, "create_callbacks"))

    callbacks.init_callbacks(callback_list)


def __destroy_callbacks():
    print("\nDestroying callbacks:")

    callbacks.destroy_callbacks()


def __create_grammars():
    global __grammars
    print("\nLoading grammars:")
    i18n.set('locale', locale)
    i18n.set('fallback', 'en')
    for unit in [u for u in __get_units() if u.grammar_name is not None]:
        translations_directory = os.path.join(os.path.dirname(__get_module_by_unit(unit).__file__), "translations")
        i18n.load_path.append(translations_directory)

        def translate(key):
            return i18n.t(unit.grammar_name + "." + key)

        grammar = Grammar(unit.grammar_name)
        enabled = __call_function(unit, "create_grammar", False, g=grammar, t=translate)
        grammar.load()
        __grammars.append(grammar)
        del i18n.load_path[:]
        # if not enabled:
        #     grammar.disable()
        print(" - %s" % grammar.name)


def __unload_grammars():
    print("\nUnloading grammars:")
    for g in __grammars:
        print(" - %s" % g.name)
        g.unload()
        __grammars.clear()


def __load_configurations():
    print("\nLoading configurations:")
    for unit in __get_units():
        __call_function(unit, "load_config", config_path=configs_directory)


def get_grammars():
    return __grammars


def get_engine_type():
    return __engine_type


def save_module_data():
    data = {}
    print("\nSaving unit data:")
    for unit in __get_units():
        to_save = __call_function(unit, "save_data")
        if to_save is not None:
            data[unit.__name__] = to_save
    return data


def load_module_data(data):
    print("\nLoading unit data:")
    for unit in __get_units():
        __call_function(unit, "load_data", data=data[module.__name__])


def load(engine_type):
    global __engine_type
    __engine_type = engine_type
    __load_modules()
    __load_configurations()
    __create_grammars()


def shutdown():
    __destroy_callbacks()
    __unload_grammars()
    __unload_modules()

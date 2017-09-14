import json
import os
import re
import shutil
import sys
import traceback
from os import path
import win32com.client


class InstallationStep:
    def can_execute(self):
        pass

    def execute(self):
        pass

    def revert(self):
        pass


class NatlinkHook:
    def __init__(self):
        self.natlink_dir = get_natlink_directory()

    def can_execute(self):
        return self.natlink_dir is not None

    def execute(self):
        shutil.copyfile('data/natlink_hook.py', path.join(self.natlink_dir, '_natlink_hook.py'))

    def revert(self):
        os.remove(path.join(self.natlink_dir, '_natlink_hook.py'))


class LogOutput:
    def __init__(self):
        self.natlink_dir = get_natlink_directory()

    def can_execute(self):
        return self.natlink_dir is not None

    def execute(self):
        natlink_main = path.join(self.natlink_dir, "core", "natlinkmain.py")
        content = None
        with open(natlink_main, 'r') as content_file:
            content = content_file.read()

        content = "from dragonfly_loader.server import Server\n" + content
        content = content.replace("natlink.displayText(text, 0)", "Server.write_output(text)")
        content = content.replace("natlink.displayText(text, 1)", "Server.write_error(text)")

        with open(natlink_main, 'w') as content_file:
            content_file.write(content)

    def revert(self):
        pass


class DragonData:
    def __init__(self):
        self.item = None
        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer, "root\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_Product Where Vendor=\"Nuance Communications Inc.\"")
        for objItem in colItems:
            if "Dragon" in objItem.Name:
                self.item = objItem
                break

    def can_execute(self):
        return self.item is not None

    def execute(self):
        version_regex = re.compile('(\\d+)\\.(\\d+)\\.(\\d+)')
        match = version_regex.match(self.item.Version)
        data = {
            "name": self.item.Name,
            "version_major": int(match.group(1)),
            "version_minor": int(match.group(2)),
            "location": path.join(self.item.InstallLocation, "Program", "natspeak.exe")
        }
        f = open("dragon_data.json", "w")
        json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()

    def revert(self):
        os.remove("dragon_data.json")


def get_natlink_directory():
    regex = re.compile('(.+?NatLink\\\\MacroSystem)\\\\core')
    natlink_dir = None
    for path_entry in sys.path:
        if "NatLink" in path_entry:
            natlink_dir = regex.match(path_entry).group(1)
    return natlink_dir


def install():
    steps = [NatlinkHook(), LogOutput(), DragonData()]
    for step in steps:
        if not step.can_execute():
            return
    for step in steps:
        try:
            step.execute()
        except Exception:
            traceback.format_exc()


def uninstall():
    steps = [NatlinkHook(), LogOutput(), DragonData()]
    for step in steps:
        try:
            step.revert()
        except Exception:
            traceback.format_exc()

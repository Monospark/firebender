import shutil

import sys

import re
from setuptools import setup, find_packages
from codecs import open
from os import path, mkdir

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dragonfly_loader',
    version='1.0.0',
    description='A tool for easier dragonfly grammar creation and usage. ',
    long_description=long_description,
    url='https://github.com/monospark/dragonfly_loader',
    author='Christopher Schnick',
    author_email='c.schnick@monospark.org',
    license='LGPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Environment :: Win32 (MS Windows)",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='dragonfly voice recogition',
    packages=find_packages(),
    install_requires=['dragonfly', 'i18n'],
    entry_points={
        'console_scripts': [
            'dragonfly_loader=dragonfly_loader.cli:main',
        ],
    }
)


def install_in_user_directory():
    home = path.expanduser('~')
    config_dir = path.join(home, "dragonfly_loader")
    if not path.exists(config_dir):
        mkdir(config_dir)

    modules_config_dir = path.join(config_dir, "config")
    if not path.exists(modules_config_dir):
        mkdir(modules_config_dir)

    shutil.copyfile('data/default_config.json', path.join(config_dir, 'config.json'))


def install_in_natlink_directory():
    natlink_dir = get_natlink_directory()
    if natlink_dir is not None:
        shutil.copyfile('data/natlink_hook.py', path.join(natlink_dir, '_natlink_hook.py'))


def change_log_output():
    natlink_dir = get_natlink_directory()
    if natlink_dir is not None:
        natlink_main = path.join(get_natlink_directory(), "core", "natlinkmain.py")
        content = None
        with open(natlink_main, 'r') as content_file:
            content = content_file.read()

        content = "from dragonfly_loader.server import Server\n" + content
        content = content.replace("natlink.displayText(text, 0)", "Server.write_output(text)")
        content = content.replace("natlink.displayText(text, 1)", "Server.write_error(text)")

        with open(natlink_main, 'w') as content_file:
            content_file.write(content)


def get_natlink_directory():
    regex = re.compile('(.+?NatLink\\\\MacroSystem)\\\\core')
    natlink_dir = None
    for path_entry in sys.path:
        if "NatLink" in path_entry:
            natlink_dir = regex.match(path_entry).group(1)
    return natlink_dir


install_in_user_directory()
install_in_natlink_directory()
change_log_output()

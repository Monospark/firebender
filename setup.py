import shutil
from setuptools import setup, find_packages
from codecs import open
from os import path, mkdir

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dragonfly_loader',
    version='1.0.0',
    description='A utility that makes it easier to create and use custom dragonfly grammars.',
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
    python_requires='>=2.6, <3',
    package_data={
        'dragonfly_loader.core': ['translations/*.yml'],
    },
    entry_points={
        'console_scripts': [
            'dragonfly_loader=dragonfly_loader.wsr_starter:main',
        ],
    }
)


def install_in_user_directory():
    home = path.expanduser('~')
    config_dir = path.join(home, "dragonfly_loader")
    if not path.exists(config_dir):
        mkdir(config_dir)

    modules_dir = path.join(config_dir, "modules")
    if not path.exists(modules_dir):
        mkdir(modules_dir)

    modules_config_dir = path.join(config_dir, "config")
    if not path.exists(modules_config_dir):
        mkdir(modules_config_dir)

    shutil.copyfile('default_config.json', path.join(config_dir, 'config.json'))


def install_in_natlink_directory():
    # TODO
    pass

install_in_user_directory()
install_in_natlink_directory()

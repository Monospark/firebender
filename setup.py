from codecs import open
from os import path
from setuptools import setup, find_packages

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

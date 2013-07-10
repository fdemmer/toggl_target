#!/usr/bin/env python

from distutils.core import setup

def requirements(filename="requirements.txt"):
    with file(filename) as f:
        return [line.strip() for line in f]

setup(name='togglcli',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=requirements(),
)

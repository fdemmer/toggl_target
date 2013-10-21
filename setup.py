#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from distutils.core import setup

import togglcli


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')
requirements = read('requirements.txt')


setup(name='togglcli',
    version=togglcli.__version__,
    description='Rough around the edges toggl.com commandline client.',
    long_description=long_description,
    license='GNU General Public License, version 2.0 (GPLv2)',
    author='@mos3abof et al.',
    url='https://github.com/fdemmer/toggl_target/',
    install_requires=requirements,
    packages = [
        'targetlib',
        'targetlib.togglapi',
        'targetlib.toggltarget',
        'targetlib.workingtime',
        'togglcli',
    ],
    scripts = [
        'scripts/target.py',
        'scripts/report.py',
    ]
)

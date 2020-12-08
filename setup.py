#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pubstats.
# Copyright (C) 2018 Penn State
#
# Pubstats is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pubstats is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pubstats.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import sys

python_requires='>=3.3'
if sys.version_info < (3, 3):
    raise RuntimeError('This package requres Python 3.3+')

setup(
    name='pubstats',
    version='0.15.0',
    packages=find_packages(exclude=['tests*']),
    license='GPLv3',
    description='Creates report on publications on authors.',
    url='https://github.com/scrim-network/pubStats-dev',
    install_requires=['prettytable', 'xhtml2pdf', 'pandas', 'xlrd'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    author='Randy Miller',
    entry_points={
        'console_scripts': ['pubstats-display=pubstats.command_line:display', 'pubstats-save=pubstats.command_line:save'],
    },
    author_email='rsm5139@psu.edu',
    include_package_data=True
)

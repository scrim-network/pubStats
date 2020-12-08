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

"""Main function for running pubstats uninstalled.

This file allows pubstats to be run as a script rather than being
imported as a module. It must be called with the '-m' flag to work.

Examples
--------
Because this is designed specifically to be run from the command-line,
these examples will focus on that.

The commands can either be called with no additional arguments, in
which case fake data will be used; or, they can be called with 2
additional arguments, in which case the first and second argument will
be the key file and data file, respectively; or, they can be called
with more than 2 arguments, in which case every argumet above 2 will be
considered a tag for filtering data.

1. Display and save fake output data to standard out:
>>> python -m pubstats

2. Display and save the report to PDF and CSV using 'key.csv' and
'data.json' as the key and data files:
>>> python -m pubstats 'key.csv' 'data.json'

3. Display and save the report using the above files, but only include
'tag1' and 'tag2' in the report:
>>> python -m pubstats 'key.csv' 'data.json' 'tag1' 'tag2'
"""

import pubstats
import sys

# With no user arguments provided, display and save report with faked
# data.
if len(sys.argv) == 1:
    pubstats.display()
    pubstats.save()
# If 2 arguments are passed, use them as the names of the key file and
# data file.
elif len(sys.argv) == 3:
    pubstats.display(key_file=sys.argv[1], data_file=sys.argv[2])
    pubstats.save(key_file=sys.argv[1], data_file=sys.argv[2])
# If 3 or more arguments are passed, use the remaining arguments as the
# desired tags for the report.
elif len(sys.argv) > 3:
    pubstats.display(key_file=sys.argv[1], data_file=sys.argv[2], tags=sys.argv[3:])
    pubstats.save(key_file=sys.argv[1], data_file=sys.argv[2], tags=sys.argv[3:])
else:
    print('Incorrent number of arguments.')

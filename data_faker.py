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

"""Creates fake data for pubstats module.

Examples
--------
1. To recreate fake data included with the package:
>>> python data_faker.py

2. To create a new set of fake data:
>>> python data_faker.py --new

Please note that the package will have to be reinstalled to use the new
fake data.
"""

from faker import Faker
import os
import sys
import csv
import json

key_file = '{}/pubstats/data/key.csv'.format(os.path.dirname(os.path.realpath(__file__)))
data_file = '{}/pubstats/data/paperpile.json'.format(os.path.dirname(os.path.realpath(__file__)))

myFactory = Faker()
# Set the seed to reproduce same fake data
if '--new' not in sys.argv:
    myFactory.random.seed(555)

# Create the key file
key = [['first', 'last', 'role', 'institution', 'field', 'department',
    'alias', 'ID']]

## We want some overlap in some categories
inst = [myFactory.company()] * 10
inst[6] = myFactory.company()
inst[7] = myFactory.company()
inst[8] = myFactory.company()
inst[9] = myFactory.company()
disc = [myFactory.job()] * 10
disc[0] = myFactory.job()
disc[1] = myFactory.job()
disc[2] = myFactory.job()
disc[3] = myFactory.job()

## Create 100 rows of data
for i in range(0,99):
    ind = i % 10
    row = []
    row.append(myFactory.first_name())
    row.append(myFactory.last_name())
    row.append(myFactory.random_digit_not_null())
    row.append(inst[ind])
    row.append(disc[ind])
    row.append(myFactory.word())
    row.append(myFactory.word())
    row.append(i + 1)
    key.append(row)

with open(key_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(key)

# Create the data file
data = []

def data_dict(names=[]):
    """Creates individual data (publication) items."""
    entry = {}
    label_list = ['label1', 'label2', 'label3']
    entry['title'] = myFactory.sentence()
    journal = myFactory.bs()
    entry['journal'] = journal
    entry['journalfull'] = journal
    entry['publisher'] = myFactory.company()
    entry['labelsNamed'] = [label_list[myFactory.random_digit() % 3]]
    entry['published'] = {'year': myFactory.year()}
    for i in range(1,6):
        if i > len(names):
            names.append({'first': myFactory.first_name(), 'last': myFactory.last_name()})
    entry['author'] = names
    return entry

## Create data for 500 publications.
for i in range(0,499):
    names = []
    # We want different amounts of overlap for variety.
    # We randomly insert key authors into the data.
    if i < 100:
        inds = []
    elif i < 200:
        inds = myFactory.random_sample(elements=(range(0,100)), length=1)
    elif i < 300:
        inds = myFactory.random_sample(elements=(range(0,100)), length=2)
    elif i < 400:
        inds = myFactory.random_sample(elements=(range(0,100)), length=3)
    else:
        inds = myFactory.random_sample(elements=(range(0,100)), length=4)
    for ind in inds:
        names.append({'first': key[ind][0], 'last': key[ind][1]})
    data.append(data_dict(names=names))

with open(data_file, 'w') as f:
    json.dump(data, f, indent=2)

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

import pandas
import csv
import io

__all__ = ['key_reader']

def key_reader(filename, return_dict=False, encoding="utf-8"):
    """Reads and encodes CSV file.

    Opens and reads a CSV file. Data will be encoded as UTF-8 by default.
    Data will be returned as a list, where each row of the file is a list
    within that list. Setting the return_dict parameter to True will convert
    rows to dict types. Specific encoding can be supplied using the encoding
    parameter.

    Parameters
    ----------
    filename : str
        Name of the CSV file
    return_dict : bool
        True -> data is returned as a ``list`` of ``dict`` with the
        header values used as key values for each row.
        False -> data is returned as a ``list`` of ``list``.
        Default is False
    encoding : str
        The file encoding (default is utf-8).

    Returns
    -------
    data
        The data from the file in the format specified by `return_dict`.
    """

    # Data to be returned.
    data = []

    if filename[-3:] == "csv":
        f = io.open(filename, encoding=encoding)
    else:
        f = io.StringIO()
        df = pandas.read_excel(filename)
        df.to_csv(path_or_buf=f, encoding=encoding)
        f.seek(0)

    reader = csv.reader(f)
    for row in reader:
        # Only adds rows with data
        if any(row):
            data.append(row)

    # Get the head values for the data.
    head = data.pop(0)

    if return_dict:
        # If dictionary format is desired, zip the lines together.
        new_data = []
        for values in data:
            new_data.append({k: v for k, v in zip(head, values)})
        data = new_data

    return data

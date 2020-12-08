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

from .helpers import Helpers
import json

__all__ = ["format_data"]

def format_data(data, translator):
    """Formats publication data.

    Completes and actions needed to format the publications data.

    Parameters
    ----------
    data
        Publications data from PubStats
    translator : dict of str: str
        Dictionay of formatted names to unique keys for authors.

    Returns
    -------
    formatted: list
        List of formatted publication data.
    """

    formatted = []
    for d in data:
        if 'author' in d:
            if _author_in_authors(d['author'], translator):
                d['matched_authors'] = _author_in_authors(d['author'], translator)
                formatted.append(d)
    return formatted

def _author_in_authors(authors, translator):
    """Returns number of matched authors."""

    n = 0
    for a in authors:
        key_string = Helpers.translated_key_from_name(a.get('first'), a.get('last'), translator)
        if key_string:
            n += 1
    return n

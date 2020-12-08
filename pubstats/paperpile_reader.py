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

import json
import io
import sys

__all__ = ['paperpile_reader']

def paperpile_reader(filename, tags=None):
    """Reads and encodes JSON file.

    Opens and reads a JSON file. Data will be encoded as UTF-8 by default.
    Data will be returned as an iterable list. Setting tags will ignore items
    that do not contain any of the tags.

    Parameters
    ----------
    filename : str
        Name of the JSON file
    tags : list of str
        A list of tags to be included (default is None which means all)
        tags are included).
    """

    # Extraneous fields in data file (will be removed)
    delete_keys = ['dup_sha1', 'sha1', 'test', 'pdf_restricted', 'incomplete', 'updated', 'autocompleted', 'id_list', 'pages', 'folders', 'collection_timestamps', 'trashed', 'original_id', 'labels', 'crawl_urls', 'citekey', 'original_citekey', 'imported', 'owner', 'attachments', 'journal_checked', 'created', 'subfolders', 'autoCleaned', 'dup_group_last', 'dup_group_first', 'owner_email', 'source_id', 'view_context_open', 'gs_bibtex', 'gs_cluster_id', 'duplicates', 'note', 'view_expanded', 'editing_note']

    with open(filename, encoding='utf-8') as f:
        data = json.load(f)

    # Delete extraneous
    for key in delete_keys:
        for item in data:
            item.pop(key, None)
    # If tags are supplied, then pubs without the tags are removed
    if tags is not None:
        remove_list = []
        for item in data:
            if 'labelsNamed' in item and not any(i in tags for i in item.get('labelsNamed')):
                remove_list.append(data.index(item))
            elif 'labelsNamed' not in item:
                remove_list.append(data.index(item))
        for i in reversed(remove_list):
            del data[i]

    return data

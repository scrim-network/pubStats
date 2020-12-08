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
import csv

__all__ = ['csv1', 'csv2']

def csv1(authors, data):
    """Saves first CSV file.

    The first CSV file contains the statistic counts for each author.

    Parameters
    ----------
    authors : dict of str: Author
        The dictionary of Author objects created in PubStats.
    data : list of dict
        The publication data created in PubStats
    """

    data_head = ['first', 'last', 'total', 'lead', 'multi_author',
                 'multi_institute', 'multi_discipline',
                 'multi_institute_single_discipline',
                 'multi_discipline_single_institute', 'cuca', 'pubs']
    # Final data to be written to file is contained in output_data
    output_data = [data_head]
    # Looping through all the author data
    for i in authors.keys():
        row = []
        row.append(authors[i].fi)
        row.append(authors[i].last)
        for j in ['pubs_author', 'pubs_lead', 'pubs_multi_author',
                  'pubs_multi_institute', 'pubs_multidisciplinary',
                  'pubs_multi_institute_single_discipline',
                  'pubs_multi_discipline_single_institute']:
            row.append(authors[i].get_len(j))
        row.append(getattr(authors[i], 'cuca'))
        authored_pubs = []
        if authors[i].has_attr('pubs_author'):
            authored_pubs = authors[i].pubs_author
        row.append([x + 1 for x in authored_pubs])
        output_data.append(row)
    _file_write('pubstats1.csv', output_data)

def csv2(authors, data, translator):
    """Saves second CSV file.

    The second CSV file contains the publications information.

    Parameters
    ----------
    authors : dict of str: Author
        The dictionary of Author objects created in PubStats.
    data : list of dict
        The publication data created in PubStats
    """

    # Final data to be written to file is contained in output_data.
    output_data = []
    data_head = ['pub']
    formatted_key_data = []
    inst_list = []
    disc_list = []
    # Looping here to create a list of all intitutions and disciplines.
    for i in authors.keys():
        formatted_key_data.append(i)
        if authors[i].inst not in inst_list:
            inst_list.append(authors[i].inst)
        if authors[i].disc not in disc_list:
            disc_list.append(authors[i].disc)
    # Head is being extended to include each author, discipline, and
    # institution.
    data_head.extend(formatted_key_data)
    data_head.extend(inst_list)
    data_head.extend(disc_list)
    output_data.append(data_head)
    # Loop through publications and create the data for the write.
    for index, pub in enumerate(data):
        row = []
        row.append(index + 1)
        scrim_authors = []
        for a in pub['author']:
            pub_author = ''
            if 'first' in a and 'last' in a:
                pub_author = Helpers.translated_key_from_name(a['first'], a['last'], translator)
            if pub_author:
                scrim_authors.append(pub_author)
        matched_authors = [None] * len(formatted_key_data)
        matched_inst = [None] * len(inst_list)
        matched_disc = [None] * len(disc_list)
        # Here we match the authors, institution, and discipline within
        # each row and give their column values a '1'
        for i in scrim_authors:
            matched_authors[formatted_key_data.index(i)] = 1
            matched_inst[inst_list.index(authors[i].inst)] = 1
            matched_disc[disc_list.index(authors[i].disc)] = 1
        row.extend(matched_authors)
        row.extend(matched_inst)
        row.extend(matched_disc)
        output_data.append(row)
    _file_write('pubstats2.csv', output_data)

def _file_write(filename, data):
    """Writes data to the file

    Parameters
    ----------
    filename : str
        The name of the file to write data to.
    data : list
        The data to be written.
    """

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

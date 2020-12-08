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
from prettytable import PrettyTable
import textwrap
import inspect

class Display():

    def __init__(self, authors, data, key):
        """Prints report to terminal window"""
        self.authors = authors
        self.data = data
        self.key = key
        self.print_string = ''
        for i in self.authors.keys():
            for item in inspect.getmembers(Display):
                if item[0][0:6] == '_block':
                    eval('self.'+item[0]+'(i)')
        self.print_string += '\nBibliography\n'
        table = PrettyTable(['n', 'bib'])
        table.header = False
        table.border = False
        table.align = 'l'
        for i, d in enumerate(self.data):
            row = [''] * 2
            row[0] = i + 1
            row[1] = textwrap.fill(self._formatted_bib(d), width=70)
            table.add_row(row)
        self.print_string += "%s\n" % (table.get_string())
        print(self.print_string)

    def _block_head(self, k):
        """Header---Author Name"""
        self.print_string += "%s %s\n\n" % (self.authors[k].fi, self.authors[k].last)

    def _block_meta(self, k):
        """Author Statistcs Part"""
        if self.authors[k].has_attr('pubs_author'):
            self.print_string += "  total publications: %d\n" % (self.authors[k].get_len('pubs_author'))
        else:
            self.print_string += "  no publications"
        if self.authors[k].has_attr('pubs_lead'):
            self.print_string += "  lead author: %d\n" % (self.authors[k].get_len('pubs_lead'))
        if self.authors[k].has_attr('pubs_multi_author'):
            self.print_string += "  multiple SCRiM authors: %d\n" % (self.authors[k].get_len('pubs_multi_author'))
        if self.authors[k].has_attr('pubs_multi_institute'):
            self.print_string += "  from multiple institutes: %d\n" % (self.authors[k].get_len('pubs_multi_institute'))
        if self.authors[k].has_attr('pubs_multidisciplinary'):
            self.print_string += "  from multiple disciplines: %d\n" % (self.authors[k].get_len('pubs_multidisciplinary'))
        if self.authors[k].has_attr('pubs_multi_institute_single_discipline'):
            self.print_string += "  multiple institutes; single discipline: %d\n" % (self.authors[k].get_len('pubs_multi_institute_single_discipline'))
        if self.authors[k].has_attr('pubs_multi_discipline_single_institute'):
            self.print_string += "  multiple disciplines; single institute: %d\n" % (self.authors[k].get_len('pubs_multi_discipline_single_institute'))
        if self.authors[k].has_attr('pubs_author'):
            self.print_string += "  cross-unit co-authorship: %d\n" % (getattr(self.authors[k], 'cuca'))

    def _block_pub(self, k):
        """Author Publications Part"""
        if self.authors[k].has_attr('pubs_author'):
            table = PrettyTable([' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', 'bib', 'n auth', 'scrim', 'non-scrim'])
            table.hrules = True
            self.print_string += '\n  Publications\n'
            for p in self.authors[k].pubs_author:
                row = [''] * 9
                if self.authors[k].pub_is_in('pubs_multi_author', p):
                    row[0] = 'X'
                if self.authors[k].pub_is_in('pubs_multi_institute', p):
                    row[1] = 'X'
                if self.authors[k].pub_is_in('pubs_multidisciplinary', p):
                    row[2] = 'X'
                if self.authors[k].pub_is_in('pubs_multi_institute_single_discipline', p):
                    row[3] = 'X'
                if self.authors[k].pub_is_in('pubs_multi_discipline_single_institute', p):
                    row[4] = 'X'
                row[5] = textwrap.fill(self._formatted_bib(self.data[p]), width=70)
                row[6] = len(self.data[p]['author'])
                row[7] = self.data[p]['matched_authors']
                row[8] = row[6] - row[7]
                table.add_row(row)
            self.print_string += "%s\n" % (table.get_string())
            self.print_string += "  1: multiple SCRiM authors\n"
            self.print_string += "  2: multiple institutes\n"
            self.print_string += "  3: multiple disciplines\n"
            self.print_string += "  4: multiple institutes; single discipline\n"
            self.print_string += "  5: multiple disciplines; single institute\n\n"

    def _block_foot(self, k):
        """Footer"""
        self.print_string += '\n'

    def _formatted_bib(self, pub):
        """Format References.

        This should be straightforward. Check for key values, then add
        them to the reference.
        """
        formatted = ''
        formatted += '%s' % (self._formatted_author(pub['author']))
        if 'year' in pub['published']:
            formatted = '%s (%s)' % (formatted, pub['published']['year'])
        else:
            formatted = '%s (%s)' % (formatted, 'n/a')
        if 'title' in pub:
            formatted = '%s: %s' % (formatted, pub['title'])
        if 'journal' in pub:
            formatted = '%s, %s' % (formatted, pub['journal'])
        elif 'journalfull' in pub:
            formatted = '%s, %s' % (formatted, pub['journalfull'])
        if 'volume' in pub and 'issue' in pub:
            formatted = '%s, %s(%s)' % (formatted, pub['volume'], pub['issue'])
        elif 'volume' in pub:
            formatted = '%s, %s' % (formatted, pub['volume'])
        if 'pages' in pub:
            formatted = '%s, %s' % (formatted, pub['pages'])
        if 'doi' in pub:
            formatted = '%s, DOI: %s' % (formatted, pub['doi'])
        formatted += '.'
        return formatted

    def _formatted_author(self, author):
        """Format author name in references."""
        formatted = ''
        auth_list = []
        for a in author:
            if 'first' in a and 'last' in a:
                auth_list.append("%s %s" % (a['first'], a['last']))
            elif 'last' in a:
                auth_list.append("%s" % (a['last']))
            else:
                auth_list.append("%s" % ('n/a'))
        formatted = ', '.join(auth_list)
        return formatted

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
import inspect
import cgi
import codecs
from xhtml2pdf import pisa

class Save():

    def __init__(self, authors, data, key):
        """Creates PDF file.

        This class creates the PDF file for the statistics report. It starts
        by creating an HTML document then converting it to PDF with xhtml2pdf.
        """
        self.authors = authors
        self.data = data
        self.key = key
        # Add CSS
        self.print_string = Save._css()
        # First Section---Authors and Statistics
        self.print_string += '<body>\n<h1>Publication Statistics</h1>\n<h2>Authors</h2>\n'
        # Runs through methods beginning with '_block'
        # for each author in the key.
        # 'i' Is the key for the author, used in author lookup.
        for i in self.authors.keys():
            for item in inspect.getmembers(Save):
                if item[0][0:6] == '_block':
                    eval('self.'+item[0]+'(i)')
        # Second Section---Bibliography
        self.print_string += '<h2>Bibliography</h2>\n'
        self.print_string += "<ol>\n"
        # Runs through each publication creating formatted bib entries
        for i, d in enumerate(self.data):
            self.print_string += "<li>{}</li>\n".format(self._formatted_bib(d))
        # Close section and document
        self.print_string += "</ol>\n</body>\n"
        self.print_string = "<html>\n{}</html>".format(self.print_string)
        # Fix problem characters
        self._problem_characters()
        with open('pubstats.pdf', 'w+b') as f:
            pisa.CreatePDF(codecs.encode(self.print_string, encoding='ascii', errors='xmlcharrefreplace'), dest=f)

    def _block_head(self, k):
        """Header---Author Name"""
        self.print_string += "<h3>{} {}</h3>\n".format(self.authors[k].fi, cgi.escape(self.authors[k].last))

    def _block_meta(self, k):
        """Author Statistcs Part"""
        # First check is to see if they authored any of the publications
        if self.authors[k].has_attr('pubs_author'):
            # Stats table starts here
            self.print_string += "<table>\n"
            self.print_string += "<tr>\n<td class='stats left'>total publications:</td><td class='stats right'>%d</td>\n</tr>\n" % (self.authors[k].get_len('pubs_author'))
            if self.authors[k].has_attr('pubs_lead'):
                self.print_string += "<tr>\n<td class='stats left'>lead author:</td><td class='stats right'>%d</td>\n</tr>\n" % (self.authors[k].get_len('pubs_lead'))
            if self.authors[k].has_attr('pubs_multi_author'):
                self.print_string += "<tr>\n<td class='stats left'>multiple SCRiM authors:</td><td class='stats right'>%d</td>\n</tr>\n" % (self.authors[k].get_len('pubs_multi_author'))
            if self.authors[k].has_attr('pubs_multi_institute'):
                self.print_string += "<tr>\n<td class='stats left'>from multiple institutes:</td><td class='stats right'>%d</td>\n</tr>\n" % (self.authors[k].get_len('pubs_multi_institute'))
            if self.authors[k].has_attr('pubs_multidisciplinary'):
                self.print_string += "<tr>\n<td class='stats left'>from multiple disciplines:</td><td class='stats right'>%d</td>\n</tr>\n" % (self.authors[k].get_len('pubs_multidisciplinary'))
            if self.authors[k].has_attr('pubs_multi_institute_single_discipline'):
                self.print_string += "<tr>\n<td class='stats left'>multiple institutes; single discipline:</td><td class='stats right'>%d</td>\n</tr>\n" % (self.authors[k].get_len('pubs_multi_institute_single_discipline'))
            if self.authors[k].has_attr('pubs_multi_discipline_single_institute'):
                self.print_string += "<tr>\n<td class='stats left'>multiple disciplines; single institute:</td><td class='stats right'>%d</td>\n</tr>\n" % (self.authors[k].get_len('pubs_multi_discipline_single_institute'))
            if self.authors[k].has_attr('cuca'):
                self.print_string += "<tr>\n<td class='stats left'>cross-unit co-authorship:</td><td class='stats right'>%d</td>\n</tr>\n" % (getattr(self.authors[k], 'cuca'))
            self.print_string += "</table>\n"
        # Else---they did not author any of the publications
        else:
            self.print_string += "<p>no publications</p>\n"

    def _block_pub(self, k):
        """Author Publications Part"""
        # First check is to see if they authored any of the publications
        if self.authors[k].has_attr('pubs_author'):
            # Publications section starts here
            self.print_string += '<h4>Publications</h4>\n'
            self.print_string += "<table border='1'>\n"
            self.print_string += "<tr>\n<th class='pubs left'>a</th><th class='pubs left'>b</th><th class='pubs left'>c</th><th class='pubs left'>d</th><th class='pubs left'>e</th><th class='pubs center'>publication</th><th class='pubs right'>n auth</th><th class='pubs right'>scrim</th><th class='pubs right'>non-scrim</th>\n</tr>\n"
            # Loops through all publications author is involved with.
            # 'p' In this case is the list index of the publication.
            for p in self.authors[k].pubs_author:
                self.print_string += "<tr>\n<td class='pubs left'>"
                # 'row' Will hold cell values for each row.
                row = [''] * 9
                # This series of 'if' statements adds 'X' to cells
                # if the publication's condition is met.
                if self.authors[k].pub_is_in('pubs_multi_author', p):
                    row[0] = '&#x25CF;'
                if self.authors[k].pub_is_in('pubs_multi_institute', p):
                    row[1] = '&#x25CF;'
                if self.authors[k].pub_is_in('pubs_multidisciplinary', p):
                    row[2] = '&#x25CF;'
                if self.authors[k].pub_is_in('pubs_multi_institute_single_discipline', p):
                    row[3] = '&#x25CF;'
                if self.authors[k].pub_is_in('pubs_multi_discipline_single_institute', p):
                    row[4] = '&#x25CF;'
                # This is the actual formatted reference.
                row[5] = "[{}] {}".format(p+1, self._formatted_bib(self.data[p]))
                # Total number of authors.
                row[6] = len(self.data[p]['author'])
                # Number of matched authors from key.
                row[7] = self.data[p]['matched_authors']
                # Number of non-key authors.
                row[8] = row[6] - row[7]
                # This section joins the rows together with HTML.
                self.print_string += "</td>\n<td class='pubs left'>".join([str(i) for i in row[0:5]])
                self.print_string += "</td>\n<td class='pubs middle'>"
                self.print_string += "</td>\n<td class='pubs middle'>".join([str(i) for i in row[5:6]])
                self.print_string += "</td>\n<td class='pubs right'>"
                self.print_string += "</td>\n<td class='pubs right'>".join([str(i) for i in row[6:]])
                self.print_string += "</td>\n</tr>\n"
            self.print_string += "</table>\n"
            # Add a caption below the table.
            self.print_string += "<br>\n<ul>\n"
            self.print_string += "<li><i>a. multiple SCRiM authors</i></li>\n"
            self.print_string += "<li><i>b. multiple institutes</i></li>\n"
            self.print_string += "<li><i>c. multiple disciplines</i></li>\n"
            self.print_string += "<li><i>d. multiple institutes; single discipline</i></li>\n"
            self.print_string += "<li><i>e. multiple disciplines; single institute</i></li>\n</ul>\n"

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
            formatted = '%s: <b>%s</b>' % (formatted, pub['title'])
        if 'journal' in pub:
            formatted = '%s, <i>%s</i>' % (formatted, pub['journal'])
        elif 'journalfull' in pub:
            formatted = '%s, <i>%s</i>' % (formatted, pub['journalfull'])
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
                formatted_name = "{} {}".format(a['first'], a['last'])
            elif 'last' in a:
                formatted_name = "{}".format(a['last'])
            else:
                formatted_name = "{}".format('n/a')
            if Helpers.translated_key_from_name(a.get('first'), a.get('last'), self.key):
                formatted_name = "<span class='highlight'>{}</span>".format(formatted_name)
            auth_list.append(formatted_name)
        formatted = ', '.join(auth_list)
        return formatted

    def _problem_characters(self):
        """Fixes some problem characters"""
        issues = [['₁', '<sub>1</sub>'],
                  ['₂', '<sub>2</sub>'],
                  ['₃', '<sub>3</sub>'],
                  ['₄', '<sub>4</sub>'],
                  ['₅', '<sub>5</sub>'],
                  ['₆', '<sub>6</sub>'],
                  ['₇', '<sub>7</sub>'],
                  ['₈', '<sub>8</sub>'],
                  ['₉', '<sub>9</sub>'],
                  ['₀', '<sub>0</sub>'],
                  ['₊', '<sub>+</sub>'],
                  ['₋', '<sub>-</sub>'],
                  ['⁰', '<sup>0</sup>'],
                  ['¹', '<sup>1</sup>'],
                  ['²', '<sup>2</sup>'],
                  ['³', '<sup>3</sup>'],
                  ['ⁱ', '<sup>i</sup>'],
                  ['⁴', '<sup>4</sup>'],
                  ['⁵', '<sup>5</sup>'],
                  ['⁶', '<sup>6</sup>'],
                  ['⁷', '<sup>7</sup>'],
                  ['⁸', '<sup>8</sup>'],
                  ['⁹', '<sup>9</sup>'],
                  ['⁺', '<sup>+</sup>'],
                  ['⁻', '<sup>-</sup>']
                  ]
        for i in issues:
            self.print_string = self.print_string.replace(i[0], i[1])

    @staticmethod
    def _css():
        """CSS for the report."""
        css_string = """<style>
        td, th {
        width: 190px;
        text-align: center;
        padding: 0px 2px 0px 2px;
        }
        th {
        height: 25px;
        }
        td.stats.left {
        text-align: right;
        }
        td.stats.right {
        width: 20px;
        text-align: left;
        }
        td.pubs.middle {
        width: 500px;
        text-align: left;
        padding: 3px;
        }
        td.pubs.left {
        width: 20px;
        padding: 3px;
        }
        td.pubs.right {
        width: 60px;
        padding: 3px;
        }
        span.highlight {
        background-color: #FFFF00;
        }
        </style>"""
        return css_string

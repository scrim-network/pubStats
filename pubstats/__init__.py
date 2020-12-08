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

"""Creates a report with certain statistics for authors and
publications.

Generates a report based on a provided author key and publication
database. This package matches authors in the key with their
publications, and reports statistics such as total number of
publications for that author, number of publications where they are the
lead author, and more. It also provides a complete bibliography of the
publications. Information is either display to a terminal, or saved as
a PDF. Two CSV files are also created with the statistics for possible
use elsewhere.

This package requires that `prettytable` and `xhtml2pdf` be installed
within the Python environment you are running this script in.

Methods
-------
save(key_file='./data/key.csv',
    data_file='./data/paperpile.json',
    tags=None)
    Save the data and report to a PDF and 2 CSV files.
display(key_file='./data/key.csv',
    data_file='./data/paperpile.json',
    tags=None)
    Prints report to the screen.

Classes
-------
PubStats(key_file, data_file, tags=None)
    The class representation of this Package.

Notes
-----
The database used for this module is based on PaperPile's exported
database, thus the exported database can be used without modification.

See: PaperPile https://paperpile.com/app
"""

from .key_reader import key_reader
from .paperpile_reader import paperpile_reader
from .author import Author
from .format_data import format_data
from .meta import Meta
from .helpers import Helpers
from .display import Display
from .csv_write import csv1, csv2
from .save import Save
import json
import inspect
import os

__author__ = "Randy Miller"
__copyright__ = "Copyright (C) 2018 Penn State"
__credits__ = ["Randy Miller", "Casey Helgeson", "Robert Nicholas"]
__license__ = "GPLv3"
__maintainer__ = "Randy Miller"
__email__ =  "rsm5139@psu.edu"
__status__ = "Development"
__url__ = "https://github.com/scrim-network/pubStats"

__all__ = ["save", "display"]

_dir = os.path.dirname(os.path.realpath(__file__))
_key_file = "{}{}".format(_dir, "/data/key.csv")
_data_file = "{}{}".format(_dir, "/data/paperpileExample.json")
#_dir = os.path.dirname('/Users/mdl5548/Documents/GitHub/pubStats-dev/pubstats/')
#_key_file = "{}{}".format(_dir, "/data/key2.csv")
#_data_file = "{}{}".format(_dir, "/data/paperpile_March_2020.json")

def save(key_file=_key_file, data_file=_data_file, tags=None):
    """Saves report as PDF and 2 CSV files.

    If no arguments are provided for key_file and data_file, report
    will be based on faked data.

    Parameters
    ----------
    key_file : str, optional
        Filename for the author key file. File must be CSV with
        specific header values. See this package's README for more
        information. (default is ./data/key.csv)
    data_file : str, optional
        Filename for the publication database. File must be able to
        be imported by the json package. For more information on
        database format, see this package's README file. (default is
        ./data/paperpile.json)
    tags : list of str, optional
        A list of tags to include in the report. Tags are represented
        in the database's 'LabelsNamed' field. If `tags` argument is not
        provided, all publications will be included. If `tags` is
        provided, only the publications with tag are included. (default
        is None)
    """

    rep = PubStats(key_file, data_file, tags=tags)
    rep.save()

def display(key_file=_key_file, data_file=_data_file, tags=None):
    """Displays report to standard out.

    If no arguments are provided for key_file and data_file, report
    will be based on faked data.

    Parameters
    ----------
    key_file : str, optional
        Filename for the author key file. File must be CSV with
        specific header values. See this package's README for more
        information. (default is ./data/key.csv)
    data_file : str, optional
        Filename for the publication database. File must be able to
        be imported by the json package. For more information on
        database format, see this package's README file. (default is
        ./data/paperpile.json)
    tags : list of str, optional
        A list of tags to include in the report. Tags are represented
        in the database's 'LabelsNamed' field. If `tags` argument is not
        provided, all publications will be included. If `tags` is
        provided, only the publications with tag are included. (default
        is None)
    """

    rep = PubStats(key_file, data_file, tags=tags)
    rep.display()

class PubStats():
    """The class implementation of the pubstats module.
    Attributes
    ----------
    key_file : str
        Filename for the author key.
    data_file : str
        Filename for the database.
    tags : list of str
        The list of tags to include in the report.
    authors : dict of str: Author
        Contains the Author objects with information and statistics
        regarding key authors, i.e. authors from `key_file`. Dictionary
        keys are either IDs from `key_file`, aliases from `key_file`,
        or the concatenated 'firstlast' names of the author, depending
        on what's available.
    translate : dict of str: str
        Contains ``str`` to ``str`` translations from concatenated
        'firstlast' author names to their key values in the `authors`
        attribute. This helps prevent authors with the same name from
        overwriting each other.
    Methods
    -------
    save()
        Save the data and report to a PDF and 2 CSV files.
    display()
        Prints report to the screen.
    """
    def __init__(self, key_file, data_file, tags=None):
        """
        Parameters
        ----------
        key_file : str
            Filename for the author key file. File must be CSV with
            specific header values. See this package's README for more
            information.
        data_file : str
            Filename for the publication database. File must be able to
            be imported by the json package. For more information on
            database format, see this package's README file.
        tags : list of str, optional
            A list of tags to include in the report. Tags are represented
            in the database's 'LabelsNamed' field. If `tags` argument is not
            provided, all publications will be included. If `tags` is
            provided, only the publications with tag are included. (default
            is None)
        """
        self.key_file = key_file
        self.data_file = data_file
        self.tags = tags
        self.authors = {}
        self.translate = {}
        self.key_data = key_reader(self.key_file, return_dict=True)
        #key_data = key_reader(key_file, return_dict=True)
        self.data = paperpile_reader(self.data_file, tags=self.tags)
        self._init_authors()
        self.formatted = format_data(self.data, self.translate)
        self._meta()
    def save(self):
        """Saves report as PDF and 2 CSV files."""
        csv_write.csv1(self.authors, self.formatted)
        csv_write.csv2(self.authors, self.formatted, self.translate)
        Save(self.authors, self.formatted, self.translate)
    def display(self):
        """Displays report to standard out."""
        Display(self.authors, self.formatted, self.translate)
    def _init_authors(self):
        """Creates the author data."""
        for i in self.key_data:
            key_formatted = Helpers.key_from_name(i.get('first'), i.get('last'))
            new_author = Author(i.get('first'), i.get('last'), i.get('role'), i.get('institution'), i.get('field'), i.get('department'), i.get('alias'))
            #key_formatted = Helpers.key_from_name(i.get('\ufefffirst'), i.get('last'))
            #new_author = Author(i.get('\ufefffirst'), i.get('last'), i.get('role'), i.get('institution'), i.get('field'), i.get('department'), i.get('alias'))
            if new_author.ID:
                self.translate[key_formatted] = new_author.ID
            elif new_author.alias:
                self.translate[key_formatted] = new_author.alias
            else:
                self.translate[key_formatted] = key_formatted
            if self.translate[key_formatted] not in self.authors:
                self.authors[self.translate[key_formatted]] = new_author
    def _meta(self):
        """Does the statistics calculations for the report."""
        for item in inspect.getmembers(Meta, predicate=inspect.isfunction):
            if item[0][0:4] == "pubs":
                for i, d in enumerate(self.formatted):
                    eval("Meta."+item[0]+"(d, self.authors, i, self.translate)")

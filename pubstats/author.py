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

import inspect

class Author():
    """Class to represent key authors.

    This class creates an Author object with the data from key.csv.
    It additionally stores author statistics and index values for
    publications that apply to those statistics. Statistics attributes
    are not pre-defined by the class itself, and are defined by the Meta
    class.

    Attributes
    ----------
    fi : str
        First name.
    last : str
        Last name.
    role : int or None
        Role within authors.
    inst : str
        Institution.
    disc : str
        Discipline.
    dept : str or None
        Department.
    alias : str or None
        Author alias ID.
    ID : str or None
        Unique ID.
    cuca : int
        Cross-unit co-authorship.
    pubs_<str> : list of int
        Related to statiscs. Lists publication indices related to each
        statistic. Created by Meta class.

    Methods
    -------
    new_pub_list(name)
        Creates a new attribute as `name`.
    get_len(name)
        Gets the length of attribute `name`
    add_pub(name, value)
        Adds a publication with index `value` to attribute `name`.
    has_attr(name)
        Returns True if attribute `name` exists.
    pub_is_in(name, n)
        Returns True if pub index `n` is in attribute `name`.
    """

    def __init__(self, fi, last, role, inst, disc, dept=None, alias=None, ID=None):
        """
        Parameters
        ----------
        fi : str
            First name.
        last : str
            Last name.
        role : int or None
            Role within authors.
        inst : str
            Institution.
        disc : str
            Discipline.
        dept : str or None
            Department. (default is None)
        alias : str or None
            Author alias ID. (default is None)
        ID : str or None
            Unique ID. (default is None)
        """

        self.fi = fi
        self.last = last
        try:
            self.role = int(role)
        except ValueError:
            self.role = None
        self.inst = inst
        self.disc = disc
        self.dept = dept
        self.alias = alias
        self.ID = ID
        self.cuca = 0

    def new_pub_list(self, name):
        """Initializes a new attribute.

        New attribute will be a list of ``int``. They point to specific
        publications.

        Parameters
        ----------
        name : str
            Name of the new attribute.
        """

        setattr(self, name, [])

    def get_len(self, name):
        """Get the lenth of an attribute.

        Parameters
        ----------
        name : str
            Name of the attribute.

        Returns
        -------
        int
            The length of the attribute.
        """

        if hasattr(self, name):
            return len(getattr(self, name))
        return 0

    def add_pub(self, name, value):
        """Adds a publication index to an attribute.

        Parameters
        ----------
        name : str
            Name of the attribute.
        value : int
            Index value of publication

        Notes
        -----
        Attribute will be created if it doesn't already exist.
        """

        if not hasattr(self, name):
            self.new_pub_list(name)
        getattr(self, name).append(value)

    def has_attr(self, name):
        """Test if attribute exists.

        Parameters
        ----------
        name : str
            Name of the attribute.

        Returns
        -------
        bool
            True if attribute exists.
        """

        if not hasattr(self, name):
            return False
        return True

    def pub_is_in(self, name, n):
        """Test if publication is in attribute.

        Parameters
        ----------
        name : str
            Name of the attribute.
        n : int
            Index of publication.

        Returns
        -------
        bool
            True if publication is in the attribute list.
        """

        if hasattr(self, name):
            return n in getattr(self, name)
        return False

    def inc_cuca(self, n):
        """Increment cuca by n.

        Parameters
        ----------
        n : int
            Number to add to cuca.
        """

        self.cuca += n

    def __repr__(self):
        string = "{}, {}, {}, {}, {}, {}, {}, {}".format(self.fi, self.last, self.role, self.inst, self.disc, self.dept, self.alias, self.ID)
        for item in inspect.getmembers(self):
            if item[0][0:4] == 'pubs':
                string = "{}\n{}: {}".format(string, item[0], item[1])
        return string

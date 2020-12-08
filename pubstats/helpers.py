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

class Helpers():
    """Some helper methods for pubstats.

    Methods
    -------
    key_from_name(fi, ln)
        Creates a formatted string to be used as a key value.
    translated_key_from_name(fi, ln, translator)
        Creates a formatted string to be used as a key value, and
        translates that string to a unique key value if applicable.
    """

    @staticmethod
    def key_from_name(fi, ln):
        """Returns formatted key value.

        Parameters
        ----------
        fi : str or None
            First name/initial of author, if applicable.
        ln : str
            Last name of author, or credited group.

        Returns
        -------
        str
            Formatted key value
        None
            Only returned if `ln` is ``None``
        """

        if fi is not None and ln is not None:
            return "{}{}".format(fi.split(' ')[0].lower().replace(' ', ''), ln.lower().replace(' ', ''))
        elif ln is not None:
            return "{}".format(ln.lower().replace(' ', ''))
        return None

    @staticmethod
    def translated_key_from_name(fi, ln, translator):
        """Returns formatted key value.

        Parameters
        ----------
        fi : str or None
            First name/initial of author, if applicable.
        ln : str
            Last name of author, or credited group.
        translator : dict of str: str
            Dictionary of values to convert keys based on a name to
            unique keys, if applicable.

        Returns
        -------
        str
            Formatted key value
        None
            If the formatted key isn't in `translator`
        """

        formatted_key = Helpers.key_from_name(fi, ln)
        if formatted_key in translator:
            return translator[formatted_key]
        return None

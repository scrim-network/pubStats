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
class Meta():
    def __init__(self):
        """Publication statistics methods.
        All methods beginning with 'pubs' will be called automatically
        by pubstats. Adding new methods will create new statistics for
        the report. Each has access to 4 arguments:
        argv[0]: Publication item (title, author, journal, etc.).
        argv[1]: Dictionary of authors (created in pubstats).
        argv[2]: Index number of publication with pubstats data
        attribute.
        argv[3]: Translator (used for author lookup).
        """
        pass
    @staticmethod
    def pubs_lead(*argv, **kwargs):
        """Checks for pub's lead author; adds it to author."""
        key = Helpers.translated_key_from_name(argv[0]['author'][0].get('first'), argv[0]['author'][0].get('last'), argv[3])
        if key:
            argv[1][key].add_pub('pubs_lead', argv[2])
    @staticmethod
    def pubs_author(*argv, **kwargs):
        """Checks for all matched authors; adds it to the authors."""
        for author in argv[0]['author']:
            key = Helpers.translated_key_from_name(author.get('first'), author.get('last'), argv[3])
            if key:
                argv[1][key].add_pub('pubs_author', argv[2])
    @staticmethod
    def pubs_coauthor(*argv, **kwargs):
        """Checks for all matched coauthors."""
        for author in argv[0]['author']:
            if argv[0]['author'].index(author) != 0:
                key = Helpers.translated_key_from_name(author.get('first'), author.get('last'), argv[3])
                if key:
                    argv[1][key].add_pub('pubs_coauthor', argv[2])
    @staticmethod
    def pubs_multi_author(*argv, **kwargs):
        """Checks for multiple matched authors."""
        key_list = Meta.get_author_list(argv[0], argv[1], argv[3])
        if len(key_list) > 1:
            for key in key_list:
                argv[1][key].add_pub('pubs_multi_author', argv[2])
    @staticmethod
    def pubs_multidisciplinary(*argv, **kwargs):
        """Checks if matched authors are from multiple disciplines."""
        key_list = Meta.get_author_list(argv[0], argv[1], argv[3])
        if Meta._is_multi(key_list, argv[1], 'disc'):
            for key in key_list:
                argv[1][key].add_pub('pubs_multidisciplinary', argv[2])
    @staticmethod
    def pubs_multi_institute(*argv, **kwargs):
        """Checks if matched authors are from multiple institutes."""
        key_list = Meta.get_author_list(argv[0], argv[1], argv[3])
        if Meta._is_multi(key_list, argv[1], 'inst'):
            for key in key_list:
                argv[1][key].add_pub('pubs_multi_institute', argv[2])
    @staticmethod
    def pubs_multi_institute_single_discipline(*argv, **kwargs):
        """Checks if from multiple institutes and single discipline."""
        key_list = Meta.get_author_list(argv[0], argv[1], argv[3])
        if Meta._is_multi(key_list, argv[1], 'inst') and not Meta._is_multi(key_list, argv[1], 'disc'):
            for key in key_list:
                argv[1][key].add_pub('pubs_multi_institute_single_discipline', argv[2])
    @staticmethod
    def pubs_multi_discipline_single_institute(*argv, **kwargs):
        """Checks if from multiple disciplines and single institute."""
        key_list = Meta.get_author_list(argv[0], argv[1], argv[3])
        if Meta._is_multi(key_list, argv[1], 'disc') and not Meta._is_multi(key_list, argv[1], 'inst'):
            for key in key_list:
                argv[1][key].add_pub('pubs_multi_discipline_single_institute', argv[2])
    @staticmethod
    def pubs_num_inst_plus_num_dist(*argv, **kwargs):
        """Sums institutes and disciplines."""
        #argv[0]: Publication item (title, author, journal, etc.). , d
        #argv[1]: Dictionary of authors (created in pubstats). , authors
        #argv[2]: Index number of publication with pubstats data attribute. ,
        #argv[3]: Translator (used for author lookup) , translate
        key_list = Meta.get_author_list(argv[0], argv[1], argv[3])
        #key_list = get_author_list(d, authors, translate)
        disc_list = []
        #key = key_list[1]
        #inst_list = []
        #disc_dict = {}
        for key in key_list:
            #disc_list.append(getattr(authors[key], 'disc').lower())
            disc_list.append(getattr(argv[1][key], 'disc').lower())
            #inst = getattr(argv[1][key], 'inst').lower()
            #inst = getattr(authors[key], 'inst').lower()
            #inst_list.append(inst)
            #disc_dict[inst] = []
        #inst_list = set(inst_list)
        disc_list = set(disc_list)
        #for key in key_list:
            #disc = getattr(argv[1][key], 'disc').lower()
            #inst = getattr(argv[1][key], 'inst').lower()
        #    disc = getattr(authors[key], 'disc').lower()
        #    inst = getattr(authors[key], 'inst').lower()
        #    disc_dict[inst].append(disc)
        #for inst in inst_list:
        #    disc_dict[inst] = set(disc_dict[inst])
        for key in key_list:
            #inst = getattr(argv[1][key], 'inst').lower()
            #argv[1][key].inc_cuca(len(inst_list) - 1)
            #argv[1][key].inc_cuca(len(disc_dict[inst]) - 1)
            argv[1][key].inc_cuca(len(disc_list) - 1)
    @staticmethod
    def get_author_list(pub, authors, translate):
        """
        Returns a list of keys. Keys are the key authors that are listed as
        authors of the pub.
        """
        key_list = []
        for author in pub['author']:
            key = Helpers.translated_key_from_name(author.get('first'), author.get('last'), translate)
            if key:
                key_list.append(key)
        return key_list
    @staticmethod
    def _is_multi(key_list, authors, name):
        """
        Determines if key list has authors from multi X, X being any given
        characteristic accounted for in the key.csv file.
        """
        for key in key_list:
            if key_list.index(key) == 0:
                val = getattr(authors[key], name)
            if val.lower() != getattr(authors[key], name).lower():
                return True
        return False

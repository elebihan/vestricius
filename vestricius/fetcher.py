# -*- coding: utf-8 -*-
#
# This file is part of vestricius
#
# Copyright (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
   vestricius.fetcher
   ``````````````````

   Abstract base class for file fetchers

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""


import abc


class Fetcher:
    """Abstract base class for fetching crash archives for a repository."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def url(self):
        """URL of the crash archive repository"""
        pass

    @abc.abstractmethod
    def lookup(self, pattern=None, count=1):
        """Looks for a crash archive in the repository

        @param pattern: regular expression of filename to look for.
        @type pattern: str

        @param count: number of results
        @type count: int

        @return: list of filenames with date of last modification
        @rtype: list of (str, str)
        """
        pass

    @abc.abstractmethod
    def fetch(self, pattern=None, dest=None, callback=None):
        """Looks for a crash archive in the repository

        @param pattern: regular expression of filename to look for.
        @type pattern: str

        @param dest: path to the output directory
        @type dest: str

        @param callback: function to call to notify transfer progress
        """
        pass

    @abc.abstractmethod
    def retrieve(self, filename, dest=None, callback=None):
        """Looks for a crash archive in the repository

        @param pattern: regular expression of filename to look for.
        @type pattern: str

        @param dest: path to the output directory
        @type dest: str

        @param callback: function to call to notify transfer progress
        """
        pass


# vim: ts=4 sw=4 sts=4 et ai

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
   vestricius.haruspex
   ```````````````````

   Provides basic Haruspex support

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import abc


class Haruspex:
    """Base abstract class for inspecting crash archive.

    This class can not be instanced directly, but must be subclassed.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        """Name of the Haruspex"""
        pass

    @abc.abstractmethod
    def inspect(self, filename):
        """Inspects a crash archive.

        @param filename: path to the crash archive file
        @type filename: str
        """
        pass

    @abc.abstractmethod
    def reveal(self, pattern):
        """Fetches and inspects latest available crash archive

        @param pattern: pattern of the crash archive name
        @type pattern: str
        """
        pass

    @abc.abstractmethod
    def peek(self, pattern):
        """Returns information about the latest available crash archive

        @param pattern: pattern of the crash archive name
        @type pattern: str

        @return: filename and date of last modification
        @rtype: (str, str)
        """
        pass

    @abc.abstractmethod
    def watch(self, duration=None, pattern=None, callback=None, data=None):
        """Watch for a new crash archive

        @param duration: number of seconds to watch for new archive, or None
        for infinite watch.
        @type duration: int

        @param pattern: regular expression for archive name
        @type pattern: str

        @param callback: function to call when a new crash archive is found
        Print to matching result on standard output if None given
        @type callback: ?

        @param data: data to to pass to the callback
        @type data: any
        """
        pass

# vim: ts=4 sw=4 sts=4 et ai

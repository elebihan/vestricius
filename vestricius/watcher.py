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
   vestricius.watcher
   ``````````````````

   Abstract base class for watchers

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import abc


class Watcher:
    """Base abstract class for watchers"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def watch(self, duration=None, pattern=None, callback=None, data=None):
        """Watch for new crash archives.

        @param duration: number of seconds to watch for new archive, or None
        for infinite watch.
        @type duration: int

        @param pattern: regular expression of filename to look for.
        @type pattern: str

        @param callback: function to call when a new crash archive is found
        Print to matching result on standard output if None given
        @type callback: ?

        @param data: data to to pass to the callback
        @type data: any
        """
        pass

# vim: ts=4 sw=4 sts=4 et ai

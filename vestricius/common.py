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
   vestricius.common
   `````````````````

   Common functions

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from gettext import gettext as _


class FileNotFoundError(Exception):
    """Exception raised when a file can not be found"""


class InvalidFileError(Exception):
    """Exception raised when a file type is not supported"""


def find_executable(executable, paths):
    """Find the needle in the haystack.

    @param executable: the needle
    @type executable: str

    @param paths: list of haystacks
    @type paths: list of str

    @return: the full path of the needle
    @rtype: str
    """
    for path in paths:
        fn = os.path.join(path, executable)
        if os.path.exists(fn):
            return fn
    raise FileNotFoundError(_("can not find {}").format(executable))


class ProgressReporter:
    """Reports progress

    @param src: name of the file transferred
    @type src: str

    @param dst: path to the destination file
    @type dst: str

    @param size: size of the file
    @type size: int

    @param callback: callback to invoke on updates
    """
    def __init__(self, src, dst, size, callback=None):
        self._src = src
        self._dst = dst
        self._size = size
        self._callback = callback
        self._nbytes = 0

    def update(self, count):
        """Updates progress

        @param count: number of bytes transferred
        @type count: int
        """
        self._nbytes += count
        percentage = int(100 * float(self._nbytes) / float(self._size))
        if self._callback:
            self._callback(self._src, self._dst, percentage)

# vim: ts=4 sw=4 sts=4 et ai

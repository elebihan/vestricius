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
import gzip
import tempfile
from .log import debug
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


class GZippedFileAdapter:
    """If file is gzipped, extract it. Otherwise do nothing"""
    def __init__(self, filename):
        if filename.endswith('.gz'):
            dst = tempfile.NamedTemporaryFile(prefix="vestricius-",
                                              delete=False)
            with gzip.open(filename) as src:
                dst.write(src.read())
            dst.close()
            self._path = dst.name
            self._need_cleanup = True
        else:
            self._path = filename
            self._need_cleanup = False

    def clean(self):
        if self._need_cleanup:
            debug(_("Removing '{}'").format(self.path))
            os.unlink(self.path)

    @property
    def path(self):
        return self._path

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.clean()

# vim: ts=4 sw=4 sts=4 et ai

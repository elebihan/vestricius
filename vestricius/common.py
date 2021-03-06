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
import re
import gzip
import tempfile
import shutil
import tarfile
from .log import debug, info
from gettext import gettext as _


class FileNotFoundError(Exception):
    """Exception raised when a file can not be found"""


class InvalidFileError(Exception):
    """Exception raised when a file type is not supported"""


class NoMatchError(Exception):
    """Exception rasied when no matching item is found"""


def find_file(pattern, paths):
    """Find the needle in the haystack.

    @param pattern: pattern for the name of the file to look for
    @type pattern: str

    @param paths: list of paths to search into
    @type paths: list of str

    @return: the full path of the needle
    @rtype: str
    """
    p = re.compile(pattern)
    for path in paths:
        msg = _("Searching for file matching '{}' in '{}'")
        debug(msg.format(pattern, path))
        for root, dirs, files in os.walk(path):
            for f in files:
                if p.match(f):
                    return os.path.join(root, f)
    raise FileNotFoundError(_("can not find '{}'").format(pattern))


def find_text(filename, pattern):
    """Look for some text matching a pattern in a file.

    @param filename: path to the file to look into
    @type filename: string

    @param pattern: regular expression the text shoudl match
    @type pattern: str

    @return: the matching text
    @rtype: str
    """
    expr = re.compile(pattern)
    with open(filename) as f:
        for line in f.readlines():
            match = expr.match(line.strip())
            if match:
                if match.lastindex:
                    index = 1
                else:
                    index = 0
                return match.group(index)
    raise NoMatchError(_("can not find text matching '{}'").format(pattern))

def format_for_shell(args):
    """Formats a list of string as a command line, suitable for shell.

    If an argument is a list of words, it will be quoted.

    @param args: list of strings

    @return: the command line
    @rtype: str
    """
    new_args = map(lambda a: '\"' + a + '\"' if ' ' in a else a, args)
    return ' '.join(new_args)


class GZippedFileAdapter:
    """Gunzip file to a temporary directory if needed"""
    def __init__(self, filename):
        if filename.endswith('.gz'):
            root, ext = os.path.splitext(os.path.basename(filename))
            folder = tempfile.mkdtemp(prefix="vestricius-")
            path = os.path.join(folder, root)
            info(_("Extracting to '{}'").format(path))
            with open(path, 'wb') as dst:
                with gzip.open(filename) as src:
                    dst.write(src.read())
            self._path = path
            self._need_cleanup = True
        else:
            self._path = filename
            self._need_cleanup = False

    def clean(self):
        keep = 'VESTRICIUS_KEEP_GUNZIPPED' in os.environ or False
        if self._need_cleanup and not keep:
            debug(_("Removing '{}'").format(self.path))
            os.unlink(self.path)
            folder = os.path.dirname(self.path)
            debug(_("Removing '{}'").format(folder))
            os.rmdir(folder)

    @property
    def path(self):
        return self._path

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.clean()


class TarballAdapter:
    """Extract tarball to to temporary directory.

    @param filename: path to the tarball
    @type filename: str
    """
    def __init__(self, filename):
        self._folder = tempfile.mkdtemp(prefix="vestricius-")
        debug(_("Extracting to '{}'").format(self._folder))
        tar = tarfile.open(filename, 'r')
        tar.extractall(self._folder)
        tar.close()

    def clean(self):
        keep = 'VESTRICIUS_KEEP_TMPDIR' in os.environ or False
        if not keep:
            debug(_("Removing '{}'").format(self._folder))
            shutil.rmtree(self._folder)

    @property
    def folder(self):
        return self._folder

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.clean()

# vim: ts=4 sw=4 sts=4 et ai

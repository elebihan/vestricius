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
   vestricius.debuggers.gdb
   ````````````````````````

   Helpers for the GNU Debugger

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from ..debugger import Debugger
from ..log import info, debug
from ..common import format_for_shell
from subprocess import check_output, STDOUT
from gettext import gettext as _


class GDBWrapper(Debugger):
    """Wraps the GNU debugger"""

    def __init__(self, executable, solib_paths=[], solib_prefix=None):
        self._exec = executable
        self._solib_paths = solib_paths
        self._solib_prefix = solib_prefix

    def generate_backtrace(self, dumpfile, programfile):
        info(_("Generating backtrace for {} using {}").format(programfile,
                                                              dumpfile))
        args = [self._exec, '-q']
        if len(self._solib_paths):
            args.append('-ex')
            args.append('set solib-search-path ' + ':'.join(self._solib_paths))
        if self._solib_prefix:
            args.append('-ex')
            args.append('set solib-absolute-prefix ' + self._solib_prefix)
        args += [
            '-ex', 'file ' + programfile,
            '-ex', 'core-file ' + dumpfile,
            '-ex', 'backtrace',
            '-ex', 'info threads',
            '-ex', 'quit'
        ]
        debug(_("Executing '{}'").format(format_for_shell(args)))
        output = check_output(args, stderr=STDOUT)
        return output.decode('utf-8', errors='replace').splitlines()

    @property
    def path(self):
        return self._exec

    @property
    def solib_paths(self):
        return self._solib_paths

    @property
    def solib_prefix(self):
        return self._solib_prefix

# vim: ts=4 sw=4 sts=4 et ai

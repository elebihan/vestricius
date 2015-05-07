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

from .debugger import Debugger
from ..log import info, debug
from subprocess import check_output, STDOUT
from gettext import gettext as _


class GDBWrapper(Debugger):
    """Wraps the GNU debugger"""

    def __init__(self, executable, solib_paths=[]):
        self._exec = executable
        self.solib_paths = solib_paths

    def generate_backtrace(self, dumpfile, programfile):
        info(_("Generating backtrace of {} using {}").format(programfile,
                                                             dumpfile))
        args = [
            self._exec, '-q',
            '-ex', 'set solib-search-path ' + ':'.join(self.solib_paths),
            '-ex', 'set solib-absolute-prefix ' + ':'.join(self.solib_paths),
            '-ex', 'file ' + programfile,
            '-ex', 'core-file ' + dumpfile,
            '-ex', 'backtrace',
            '-ex', 'info threads',
            '-ex', 'quit'
        ]
        debug(_("Executing '{}'").format(' '.join(args)))
        output = check_output(args, stderr=STDOUT)
        return output.decode('utf-8', errors='replace').splitlines()

    @property
    def path(self):
        return self._exec

# vim: ts=4 sw=4 sts=4 et ai

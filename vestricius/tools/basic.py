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
   vestricius.tools.basic
   ``````````````````````

   Basic set of tools for dissecting crash archives

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from vestricius.log import info
from vestricius.elf import parse_core_dump_file
from vestricius.common import find_file
from vestricius.debugger import ProgramCrashInfo
from gettext import gettext as _


class CoreDumpAnalyzer:
    """Analyzes a core dump file"""
    def __init__(self, debugger):
        self._debugger = debugger
        self.search_paths = debugger.solib_paths

    @property
    def debugger(self):
        return self._debugger

    def analyze(self, filename):
        """Perform the analysis.

        @param filename: path to the core dump file
        @type filename: str

        @return: information about the crash
        @rtype; :class:`ProgramCrashInfo`
        """
        core_info = parse_core_dump_file(filename)
        executable = core_info.process_info.name
        info(_("Core dump file generated by '{}'").format(executable))
        path = find_file(executable, self.search_paths)
        info(_("Using {} as reference").format(path))
        lines = self._debugger.generate_backtrace(filename, path)
        return ProgramCrashInfo(executable=executable,
                                core_dump=os.path.basename(filename),
                                backtrace=lines)

# vim: ts=4 sw=4 sts=4 et ai

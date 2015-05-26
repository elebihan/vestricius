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
   vestricius.plugins.simple
   `````````````````````````

   Plugin to inspect simple core dump files

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from vestricius.plugin import Plugin
from vestricius.haruspex import Haruspex
from vestricius.log import info
from vestricius.elf import parse_core_dump_file
from vestricius.common import find_executable
from vestricius.debuggers.gdb import GDBWrapper
from vestricius.report import Report
from gettext import gettext as _

_PRESET_TEXT = """
[Debugger]
Executable = gdb
SearchPaths = /usr/lib
SolibPrefix = /usr/lib
"""


class SimpleCorePlugin(Plugin):
    """Plugin for simple core dump files"""
    def __init__(self):
        pass

    @property
    def name(self):
        return 'simple-core'

    @property
    def description(self):
        return 'Plugin for simple core dump files'

    @property
    def preset_text(self):
        return _PRESET_TEXT

    def create_haruspex(self, preset):
        executable = preset.get_path('Debugger', 'Executable')
        paths = preset.get_list('Debugger', 'SearchPaths')
        prefix = preset.get_path('Debugger', 'SolibPrefix', None)
        search_paths = [os.path.expanduser(p) for p in paths]
        return SimpleCoreHaruspex(executable, search_paths, prefix)


class SimpleCoreHaruspex(Haruspex):
    def __init__(self, debugger, search_paths=[], prefix=None):
        self._debugger = GDBWrapper(debugger, search_paths, prefix)
        self._search_paths = search_paths

    def inspect(self, filename):
        core_info = parse_core_dump_file(filename)
        executable = core_info.process_info.name
        info(_("Core dump file generated by '{}'").format(executable))
        path = find_executable(executable, self._search_paths)
        info(_("Using {} as reference").format(path))
        lines = self._debugger.generate_backtrace(filename, path)
        report = Report(filename, 'simple-core')
        report.executable = executable
        report.coredump = filename
        report.debugger = self._debugger.path
        report.backtrace = lines
        return report

    def reveal(self, pattern):
        raise NotImplementedError(_("command not implemented"))

# vim: ts=4 sw=4 sts=4 et ai

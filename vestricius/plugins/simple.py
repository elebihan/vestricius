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
import tempfile
import gzip
from vestricius.plugin import Plugin
from vestricius.haruspex import Haruspex
from vestricius.log import info, debug
from vestricius.elf import parse_core_dump_file
from vestricius.common import find_executable
from vestricius.debuggers.gdb import GDBWrapper
from vestricius.report import Report
from vestricius.fetchers.ftp import FtpFetcher
from gettext import gettext as _

_PRESET_TEXT = """
[Debugger]
Executable = gdb
SearchPaths = /usr/lib
SolibPrefix = /usr/lib

[Repository]
URL = ftp://username:password@someserver/somewhere/
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
        repo_url = preset.get('Repository', 'URL')
        return SimpleCoreHaruspex(executable, search_paths, prefix, repo_url)


class SimpleCoreHaruspex(Haruspex):
    def __init__(self, debugger, search_paths=[], prefix=None, repo_url=None):
        self._debugger = GDBWrapper(debugger, search_paths, prefix)
        self._search_paths = search_paths
        self._repo_url = repo_url

    def inspect(self, filename):
        if filename.endswith('.gz'):
            dst = tempfile.NamedTemporaryFile(prefix='vestricius-simple-', delete=False)
            with gzip.open(filename) as src:
                dst.write(src.read())
            dst.close()
            core_dump = dst.name
            need_cleanup = True
        else:
            core_dump = filename
            need_cleanup = False
        core_info = parse_core_dump_file(core_dump)
        executable = core_info.process_info.name
        info(_("Core dump file generated by '{}'").format(executable))
        path = find_executable(executable, self._search_paths)
        info(_("Using {} as reference").format(path))
        lines = self._debugger.generate_backtrace(core_dump, path)
        report = Report(filename, 'simple-core')
        report.executable = executable
        report.coredump = core_dump
        report.debugger = self._debugger.path
        report.backtrace = lines
        if need_cleanup:
            debug(_("Removing '{}'").format(filename))
            os.unlink(filename)
        return report

    def reveal(self, pattern):
        if not self._repo_url:
            raise RuntimeError(_("URL of repository not set in preset"))
        fetcher = FtpFetcher(self._repo_url)
        fn = fetcher.lookup(pattern)
        info(_("Found '{}'").format(fn))
        fn = fetcher.retrieve(fn, tempfile.gettempdir())
        self.inspect(fn)

# vim: ts=4 sw=4 sts=4 et ai

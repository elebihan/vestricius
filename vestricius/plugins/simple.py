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
from vestricius.report import Report
from vestricius.log import info, debug
from vestricius.elf import parse_core_dump_file
from vestricius.common import find_executable
from vestricius.debugger import ProgramCrashInfo
from vestricius.debuggers.gdb import GDBWrapper
from vestricius.report import Report
from vestricius.fetchers.ftp import FTPFetcher
from vestricius.watchers.ftp import FTPWatcher
from gettext import gettext as _

_PRESET_TEXT = """
[Debugger]
Executable = gdb
SearchPaths = /usr/lib
SolibPrefix = /usr/lib

[Repository]
URL = ftp://username:password@someserver/somewhere/
"""

_NAME = 'simple-core'

_REPORT_YAML_TEMPLATE = """
core-dump: {{coredump}}
executable: {{executable}}
debugger: {{debugger}}
backtrace: |
{{#backtrace_lines}}
  {{backtrace_line}}
{{/backtrace_lines}}
"""


class SimpleCorePlugin(Plugin):
    """Plugin for simple core dump files"""
    def __init__(self):
        pass

    @property
    def name(self):
        return _NAME

    @property
    def description(self):
        return 'Plugin for simple core dump files'

    @property
    def preset_text(self):
        return _PRESET_TEXT

    def create_haruspex(self, preset):
        debugger = self._create_debugger(preset)
        repo_url = preset.get('Repository', 'URL')
        return SimpleCoreHaruspex(debugger, repo_url)

    def _create_debugger(self, preset):
        executable = preset.get_path('Debugger', 'Executable')
        paths = preset.get_list('Debugger', 'SearchPaths')
        prefix = preset.get_path('Debugger', 'SolibPrefix', None)
        search_paths = [os.path.expanduser(p) for p in paths]
        return GDBWrapper(executable, search_paths, prefix)


class SimpleCoreHaruspex(Haruspex):
    def __init__(self, debugger, repo_url=None):
        self._debugger = debugger
        self._search_paths = debugger.solib_paths
        self._repo_url = repo_url

    @property
    def name(self):
        return _NAME

    @property
    def search_paths(self):
        return self._search_paths

    def inspect(self, filename):
        crash_info = self.analyze_core_dump(filename)
        return self.create_report(filename, crash_info)

    def reveal(self, pattern):
        fetcher = self._create_fetcher()
        fn, date = fetcher.lookup(pattern)
        info(_("Found '{}' ({})").format(fn, date))
        fn = fetcher.retrieve(fn,
                              tempfile.gettempdir(),
                              self._on_block_received)
        report = self.inspect(fn)
        debug(_("Removing '{}'").format(fn))
        return report

    def _on_block_received(self, n_blocks, block_size, n_bytes):
        count = n_blocks * block_size
        if n_bytes == -1:
            n_kbytes = int(count / 1024)
            if count % 100 == 0:
                debug(_("Downloading file ({} KB)").format(n_kbytes))
        else:
            percentage = int(float(count) / float(n_bytes) * 100)
            if percentage % 10 == 0:
                debug(_("Downloading file ({} %)").format(percentage))

    def _create_fetcher(self):
        if not self._repo_url:
            raise RuntimeError(_("URL of repository not set in preset"))
        return FTPFetcher(self._repo_url)

    def peek(self, pattern):
        fetcher = self._create_fetcher()
        return fetcher.lookup(pattern)

    def analyze_core_dump(self, filename):
        if filename.endswith('.gz'):
            prefix = "vestricius-{}-".format(self.name)
            dst = tempfile.NamedTemporaryFile(prefix=prefix, delete=False)
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
        path = find_executable(executable, self.search_paths)
        info(_("Using {} as reference").format(path))
        lines = self._debugger.generate_backtrace(core_dump, path)
        if need_cleanup:
            debug(_("Removing '{}'").format(core_dump))
            os.unlink(core_dump)
        return ProgramCrashInfo(executable=executable,
                                core_dump=os.path.basename(filename),
                                backtrace=lines)

    def create_report(self, filename, crash_info):
        report = SimpleCoreReport(filename, self.name)
        report.executable = crash_info.executable
        report.debugger = self._debugger.path
        report.coredump = crash_info.core_dump
        report.backtrace = crash_info.backtrace
        return report

    def _create_watcher(self):
        if not self._repo_url:
            raise RuntimeError(_("URL of repository not set in preset"))
        return FTPWatcher(self._repo_url)

    def watch(self, duration=None, pattern=None, callback=None, data=None):
        watcher = self._create_watcher()
        watcher.watch(duration, pattern, callback, data)


class SimpleCoreReport(Report):
    def __init__(self, filename, plugin):
        Report.__init__(self, filename, plugin)
        self.backtrace = []
        self.executable = None
        self.debugger = None
        self.coredump = None

    @property
    def template(self):
        return Report.template.fget(self) + _REPORT_YAML_TEMPLATE

    @property
    def data(self):
        backtrace_lines = [{'backtrace_line': l} for l in self.backtrace]
        extra = {
            'coredump': self.coredump,
            'executable': self.executable,
            'debugger': self.debugger,
            'backtrace_lines': backtrace_lines,
        }
        data = Report.data.fget(self).copy()
        data.update(extra)
        return data

# vim: ts=4 sw=4 sts=4 et ai

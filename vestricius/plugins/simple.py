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
from vestricius.plugin import Plugin
from vestricius.haruspex import Haruspex
from vestricius.report import Report
from vestricius.log import info, debug
from vestricius.common import GZippedFileAdapter, FileNotFoundError
from vestricius.debuggers.gdb import GDBWrapper
from vestricius.tools.basic import CoreDumpAnalyzer
from vestricius.fetchers.factory import create_fetcher
from vestricius.watchers.factory import create_watcher
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
crash-info:
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
        toolbox = self._create_toolbox(preset)
        repo_url = preset.get('Repository', 'URL')
        return SimpleCoreHaruspex(toolbox, repo_url)

    def _create_debugger(self, preset):
        executable = preset.get_path('Debugger', 'Executable')
        paths = preset.get_list('Debugger', 'SearchPaths')
        prefix = preset.get_path('Debugger', 'SolibPrefix', None)
        search_paths = [os.path.expanduser(p) for p in paths]
        return GDBWrapper(executable, search_paths, prefix)

    def _create_toolbox(self, preset):
        toolbox = {}
        debugger = self._create_debugger(preset)
        toolbox['core-dump-analyzer'] = CoreDumpAnalyzer(debugger)
        return toolbox


class SimpleCoreHaruspex(Haruspex):
    def __init__(self, toolbox, repo_url):
        self._analyzer = toolbox['core-dump-analyzer']
        self._repo_url = repo_url

    @property
    def name(self):
        return _NAME

    @property
    def search_paths(self):
        return self._analyzer.search_paths

    def inspect(self, filename):
        crash_info = self.analyze_core_dump(filename)
        return self.create_report(filename, crash_info)

    def reveal(self, pattern):
        fetcher = create_fetcher(self._repo_url)
        results = fetcher.lookup(pattern)
        if not results:
            raise FileNotFoundError(_("no matching file found"))
        fn, date = results[0]
        info(_("Found '{}' ({})").format(fn, date))
        fn = fetcher.retrieve(fn,
                              tempfile.gettempdir(),
                              self._on_block_received)
        report = self.inspect(fn)
        keep = 'VESTRICIUS_KEEP_DOWNLOADED' in os.environ or False
        if not keep:
            debug(_("Removing '{}'").format(fn))
            os.unlink(fn)
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

    def peek(self, pattern, count):
        fetcher = create_fetcher(self._repo_url)
        return fetcher.lookup(pattern, count)

    def analyze_core_dump(self, filename):
        bn = os.path.basename(filename)
        info(_("Analyzing core dump file '{}'").format(bn))
        with GZippedFileAdapter(filename) as dump:
            return self._analyzer.analyze(dump.path)

    def create_report(self, filename, crash_info):
        report = SimpleCoreReport(filename, self.name)
        report.executable = crash_info.executable
        report.debugger = self._analyzer.debugger.path
        report.coredump = crash_info.core_dump
        report.backtrace = crash_info.backtrace
        return report

    def watch(self, duration=None, pattern=None, callback=None, data=None):
        watcher = create_watcher(self._repo_url)
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
        base = Report.template.fget(self).strip()
        return base + _REPORT_YAML_TEMPLATE

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

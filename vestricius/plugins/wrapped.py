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
   vestricius.plugins.wrapped
   ``````````````````````````

   Plugin to inspect core dump files wrapped in a tarball

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from vestricius.plugins.simple import SimpleCorePlugin, SimpleCoreHaruspex
from vestricius.common import TarballAdapter, find_file
from vestricius.log import info
from gettext import gettext as _


_PRESET_TEXT = """
[Debugger]
Executable = gdb
SearchPaths = /usr/lib
SolibPrefix = /usr/lib

[Repository]
URL = ftp://username:password@someserver/somewhere/

[Hints]
CorePattern = ^core.+(?:\.gz)?
"""

_NAME = 'wrapped-core'


class WrappedCorePlugin(SimpleCorePlugin):
    """Plugin for core dump file wrapped in a tarball"""
    def __init__(self):
        pass

    @property
    def name(self):
        return _NAME

    @property
    def description(self):
        return 'Plugin for core dump file wrapped in a tarball'

    @property
    def preset_text(self):
        return _PRESET_TEXT

    def create_haruspex(self, preset):
        toolbox = self._create_toolbox(preset)
        repo_url = preset.get('Repository', 'URL')
        pattern = preset.get('Hints', 'CorePattern', '^core.+(?:\.gz)?')
        return WrappedCoreHaruspex(pattern, toolbox, repo_url)


class WrappedCoreHaruspex(SimpleCoreHaruspex):
    def __init__(self, pattern, toolbox, repo_url):
        SimpleCoreHaruspex.__init__(self, toolbox, repo_url)
        self._core_pattern = pattern

    @property
    def name(self):
        return _NAME

    def inspect(self, filename):
        with TarballAdapter(filename) as tarball:
            fn = find_file(self._core_pattern, [tarball.folder])
            crash_info = self.analyze_core_dump(fn)
            return self.create_report(filename, crash_info)

# vim: ts=4 sw=4 sts=4 et ai

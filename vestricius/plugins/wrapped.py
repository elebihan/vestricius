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
   `````````````````````````

   Plugin to inspect core dump files wrapped in a tarball

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import re
from vestricius.plugins.simple import SimpleCorePlugin, SimpleCoreHaruspex
from vestricius.common import TarballAdapter
from vestricius.log import info, debug
from gettext import gettext as _


_PRESET_TEXT = """
[Debugger]
Executable = gdb
SearchPaths = /usr/lib
SolibPrefix = /usr/lib

[Repository]
URL = ftp://username:password@someserver/somewhere/

[Extra]
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

    def create_haruspex(self, preset):
        debugger = self._create_debugger(preset)
        repo_url = preset.get('Repository', 'URL')
        pattern = preset.get('Extra', 'CorePattern', '^core.+(?:\.gz)?')
        return WrappedCoreHaruspex(pattern, debugger, repo_url)


class WrappedCoreHaruspex(SimpleCoreHaruspex):
    def __init__(self, pattern, debugger, repo_url=None):
        SimpleCoreHaruspex.__init__(self, debugger, repo_url)
        self._core_pattern = pattern

    @property
    def name(self):
        return _NAME

    def inspect(self, filename):
        with TarballAdapter(filename) as tarball:
            fn = self._find_core_dump(tarball.folder)
            info(_("Found core dump file '{}'").format(os.path.basename(fn)))
            crash_info = self.analyze_core_dump(fn)
            return self.create_report(filename, crash_info)

    def _find_core_dump(self, workdir):
        for root, dirs, files in os.walk(workdir):
            for f in files:
                if re.match(self._core_pattern, f):
                    return os.path.join(root, f)

# vim: ts=4 sw=4 sts=4 et ai

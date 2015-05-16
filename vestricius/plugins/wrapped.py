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
import tarfile
import tempfile
import shutil
from vestricius.plugins.simple import SimpleCorePlugin, SimpleCoreHaruspex
from vestricius.log import info, debug
from gettext import gettext as _


class WrappedCorePlugin(SimpleCorePlugin):
    """Plugin for core dump file wrapped in a tarball"""
    def __init__(self):
        pass

    @property
    def name(self):
        return 'wrapped-core'

    @property
    def description(self):
        return 'Plugin for core dump file wrapped in a tarball'

    def create_haruspex(self, preset):
        debugger = preset.get('Tools', 'Debugger')
        paths = preset.get_list('Tools', 'SearchPaths')
        search_paths = [os.path.expanduser(p) for p in paths]
        return WrappedCoreHaruspex(debugger, search_paths)


class WrappedCoreHaruspex(SimpleCoreHaruspex):
    def __init__(self, debugger, search_paths=[]):
        SimpleCoreHaruspex.__init__(self, debugger, search_paths)

    def inspect(self, filename):
        workdir = self._extract(filename)
        dumpfile = self._find_core_dump(workdir)
        info(_("Found cored ump file '{}'").format(os.path.basename(dumpfile)))
        report = SimpleCoreHaruspex.inspect(self, dumpfile)
        shutil.rmtree(workdir)
        return report

    def _extract(self, path):
        workdir = tempfile.mkdtemp(prefix='vestricius-wrapped-')
        debug(_("Extracting to '{}'").format(workdir))
        tar = tarfile.open(path, 'r')
        tar.extractall(workdir)
        tar.close()
        return workdir

    def _find_core_dump(self, workdir):
        for root, dirs, files in os.walk(workdir):
            for f in files:
                if re.match(r'^core.+(?:\.gz)?', f):
                    return os.path.join(root, f)

# vim: ts=4 sw=4 sts=4 et ai

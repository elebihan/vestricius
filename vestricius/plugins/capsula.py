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
   vestricius.plugins.capsula
   ``````````````````````````

   Plugin for inspecting a tarball containing a core dump and other files.

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from vestricius.plugins.simple import SimpleCorePlugin, SimpleCoreHaruspex
from vestricius.common import TarballAdapter, find_file, find_text
from vestricius.log import debug, info, warning
from gettext import gettext as _


_PRESET_TEXT = """
[Debugger]
Executable = gdb
SearchPaths = /usr/lib,/some/path/@VERSION@/folder
SolibPrefix = /usr/lib

[Repository]
URL = ftp://username:password@someserver/somewhere/

[Hints]
CorePattern = ^core.+(?:\.gz)?
VersionFile = version.txt
VersionPattern = version=(.+)
"""

_NAME = 'capsula'


class CapsulaPlugin(SimpleCorePlugin):
    """Plugin for inspecting a tarball filled with dumps and logs.

    This plugin will look for a file containing a version string.
    If any search path defined in the preset contains the pattern '@VERSION@',
    it will be replaced by the version found.
    """
    def __init__(self):
        pass

    @property
    def name(self):
        return _NAME

    @property
    def description(self):
        return 'Plugin for tarball filled with dumps and logs'

    @property
    def preset_text(self):
        return _PRESET_TEXT

    def create_haruspex(self, preset):
        toolbox = self._create_toolbox(preset)
        hints = self._create_hints(preset)
        repo_url = preset.get('Repository', 'URL')
        return CapsulaHaruspex(hints, toolbox, repo_url)

    def _create_hints(self, preset):
        hints = {}
        hints['core-pattern'] = preset.get('Hints',
                                           'CorePattern',
                                           '^core.+(?:\.gz)?')
        hints['version-file'] = preset.get('Hints', 'VersionFile')
        hints['version-pattern'] = preset.get('Hints', 'VersionPattern')
        return hints


class CapsulaHaruspex(SimpleCoreHaruspex):
    def __init__(self, hints, toolbox, repo_url):
        SimpleCoreHaruspex.__init__(self, toolbox, repo_url)
        self._hints = hints

    @property
    def name(self):
        return _NAME

    def inspect(self, filename):
        with TarballAdapter(filename) as tarball:
            fn = find_file(self._hints['version-file'], [tarball.folder])
            debug(_("Looking for version string in '{}'").format(fn))
            version = find_text(fn, self._hints['version-pattern'])

            paths = []
            for p in self._analyzer.search_paths:
                path = p.replace('@VERSION@', version)
                if not os.path.exists(path):
                    warning(_("'{}' is not a valid path").format(path))
                paths.append(path)
            self._analyzer.search_paths = paths

            info(_("Found version '{}'").format(version))
            fn = find_file(self._hints['core-pattern'], [tarball.folder])
            crash_info = self.analyze_core_dump(fn)
            return self.create_report(filename, crash_info)

# vim: ts=4 sw=4 sts=4 et ai

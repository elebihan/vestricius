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
   vestricius.presets
   ``````````````````

   Preset management

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os

def _load_presets(path):
    """Loads presets

    @param path: path to the presets directory
    @type path: str

    @returns: list of presets
    """
    presets = []
    for entry in os.listdir(path):
        fn = os.path.join(path, entry)
        if fn.endswith('.conf'):
            presets.append(Preset(fn))
    return presets


class PresetManager:
    """Manages presets"""
    def __init__(self):
        self._presets_dir = os.path.expanduser('~/.config/vestricius.d')
        self._presets = _load_presets(self._presets_dir)

    @property
    def presets(self):
        """List of presets"""
        return self._presets

    def create(self, module, preset):
        """Create a new preset for a module.

        @param module: name of the module
        @type module: str

        @param preset: name of the new preset
        @type preset: str
        """
        pass

    def edit(self, preset):
        """Edit an existing preset

        @param preset: name of the preset to edit
        @type preset: str
        """
        pass


class Preset:
    """Holds the pre-defined configuration of a module.

    @param path: path to the preset configuration file
    @type path: str
    """
    def __init__(self, path):
        self._path = path
        self._name = None
        self._module = None

    @property
    def name(self):
        return self._name

    @property
    def module(self):
        return self._module

# vim: ts=4 sw=4 sts=4 et ai

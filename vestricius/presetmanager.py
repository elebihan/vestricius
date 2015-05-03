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
   vestricius.presetmanager
   ````````````````````````

   Preset management

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from subprocess import check_call
from gettext import gettext as _
from .pluginmanager import PluginManager
from .preset import Preset


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
        self._editor = os.environ.get('$EDITOR', 'vi')
        self._presets_dir = os.path.expanduser('~/.config/vestricius.d')
        if not os.path.exists(self._presets_dir):
            os.makedirs(self._presets_dir)
            presets = []
        else:
            presets = _load_presets(self._presets_dir)
        self._presets = presets

    @property
    def presets(self):
        """List of presets"""
        return self._presets

    def create(self, plugin_name, preset_name):
        """Create a new preset for a plugin.

        @param plugin_name: name of the plugin
        @type plugin_name: str

        @param preset_name: name of the new preset
        @type preset_name: str
        """
        preset = None
        try:
            preset = self.lookup_by_name(preset_name)
        except:
            pass
        if preset:
            raise RuntimeError(_("preset already exists"))

        plugin_mgr = PluginManager()
        plugin = plugin_mgr.lookup_by_name(plugin_name)

        fn = os.path.join(self._presets_dir, preset_name + '.conf')
        preset = plugin.create_preset(preset_name, fn)

        check_call([self._editor, preset.path])
        self._presets.append(preset)

    def edit(self, name):
        """Edit an existing preset

        @param name: name of the preset to edit
        @type name: str
        """
        preset = self.lookup_by_name(name)
        check_call([self._editor, preset.path])

    def lookup_by_name(self, name):
        """Finds a preset by its name.

        @param name: name of the preset
        @type name: str
        """
        for preset in self._presets:
            if preset.name == name:
                return preset
        raise RuntimeError(_("preset not found"))

    def remove(self, name):
        """Removes a preset.

        @param name: name of the preset to remove
        @type name: str
        """
        preset = self.lookup_by_name(name)
        os.unlink(preset.path)

# vim: ts=4 sw=4 sts=4 et ai

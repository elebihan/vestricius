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
   vestricius.plugin
   `````````````````

   Extension for Vestricius

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from .preset import Preset


_PRESET_TEMPLATE = """[Preset]
Name = {name}
Plugin = {plugin.name}
"""


class Plugin:
    """Extension for Vestricius"""
    def __init__(self):
        self._name = 'unknown'

    @property
    def name(self):
        """Name of the plugin"""
        return self._name

    def create_preset(self, name, path):
        """Creates a new preset for the plugin.

        @param name: name of the new preset
        @type name: str

        @param path: path of the new preset
        @type path: str

        @returns: a preset
        """
        with open(path, 'w+') as f:
            text = _PRESET_TEMPLATE.format(name=name, plugin=self)
            f.write(text)
        return Preset(path)

# vim: ts=4 sw=4 sts=4 et ai
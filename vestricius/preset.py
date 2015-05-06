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
   vestricius.preset
   `````````````````

   Predefined settings for a plugin

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from configparser import ConfigParser


class Preset:
    """Holds the pre-defined configuration of a plugin.

    @param path: path to the preset configuration file
    @type path: str
    """
    def __init__(self, path):
        self._path = path
        self._parser = ConfigParser()
        with open(path) as f:
            self._parser.read_file(f)
        self._name = self._parser.get('Preset', 'Name')
        self._plugin = self._parser.get('Preset', 'Plugin')

    @property
    def name(self):
        return self._name

    @property
    def plugin(self):
        return self._plugin

    @property
    def path(self):
        return self._path

    def get(self, section, option):
        """Gets an option value from the named section.

        @param section: name of the section
        @type section: str

        @param option: name of the option
        @type option: str

        @return: the value of the option
        @rtype: str
        """
        return self._parser.get(section, option)

    def get_list(self, section, option):
        """A convenience method which coerces the option in the specified
        section to a list of strings.

        @param section: name of the section
        @type section: str

        @param option: name of the option
        @type option: str

        @return: the value of option as a list of strings
        @rtype: list
        """
        value = self._parser.get(section, option)
        return [s.strip() for s in value.split(',')]


# vim: ts=4 sw=4 sts=4 et ai

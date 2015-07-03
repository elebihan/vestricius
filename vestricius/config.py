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
   vestricius.config
   `````````````````

   Provides configuration files management

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
from configparser import ConfigParser


class Configuration:
    """Stores the configuration of the application"""
    def __init__(self):
        self.default_preset = None
        self.default_plugin = None
        self.plugins_paths = []

    def load_from_file(self, filename):
        """Loads the configuration from a file

        @param filename: path to the configuration file to read
        @type filename: str
        """
        parser = ConfigParser()
        with open(filename) as f:
            parser.read_file(f)
        self.default_plugin = parser.get('General',
                                         'DefaultPlugin',
                                         fallback=None)
        self.default_preset = parser.get('General',
                                         'DefaultPreset',
                                         fallback=None)
        value = parser.get('General', 'PluginsPaths', fallback=None)
        if value:
            self.plugins_paths += map(lambda p: os.path.expanduser(p.strip()),
                                      value.split(','))

    def save_to_file(self, filename):
        """Saves the configuration to a file

        @param filename: path to the configuration file to create
        @type filename: str
        """
        parser = ConfigParser()
        parser.set('General', 'DefaultPlugin', self.default_plugin)
        parser.set('General', 'DefaultPreset', self.default_preset)
        parser.set('General', 'PluginsPaths', ','.join(self.plugins_paths))
        with open(filename, 'w+') as f:
            parser.write(f)

# vim: ts=4 sw=4 sts=4 et ai

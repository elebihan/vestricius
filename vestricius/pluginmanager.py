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
   vestricius.pluginmanager
   ````````````````````````

   Plugin management

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import imp
import inspect
from .log import debug
from .plugin import Plugin
from gettext import gettext as _


def find_plugins(path):
    """Finds all plugins in a path.

    @param path: path where to look for plugins
    @type path: str
    """
    plugins = []
    for fn in os.listdir(path):
        fp = os.path.join(path, fn)
        module_name, ext = os.path.splitext(fn)
        if os.path.isfile(fp) and ext == '.py':
            f, p, d = imp.find_module(module_name, [path])
            plugin_module = imp.load_module(module_name, f, p, d)
            plugin_classes = inspect.getmembers(plugin_module, inspect.isclass)
            for name, klass in plugin_classes:
                if issubclass(klass, Plugin):
                    if klass.__module__ == module_name:
                        plugins.append(klass())

    return plugins


class PluginManager:
    """Manages plugins

    @param scan: if True, scan search paths for plugins
    @type scan: bool
    """
    def __init__(self, scan=True):
        path = os.path.dirname(os.path.abspath(__file__))
        plugin_dir = os.path.join(path, 'plugins')
        self._search_paths = [plugin_dir]
        self._plugins = []
        if scan:
            self.scan_plugins()

    def add_search_path(self, path):
        """Adds a new path for searching plugins.

        @param path: path where to look for new plugins
        @type path: str
        """
        self._search_paths.append(path)

    def scan_plugins(self):
        """Scans all known search paths for plugins"""
        self._plugins = []
        for path in self._search_paths:
            debug(_("Searching for plugins in {}").format(path))
            plugins = find_plugins(path)
            for plugin in plugins:
                debug(_("Found plugin '{}'").format(plugin.name))
            self._plugins += plugins

    @property
    def plugins(self):
        """List of plugins"""
        return self._plugins

    def lookup_by_name(self, name):
        """Finds a plugin by its name.

        @param name: name of the plugin
        @type name: str
        """
        for plugin in self._plugins:
            if plugin.name == name:
                return plugin
        raise RuntimeError(_("plugin not found"))

# vim: ts=4 sw=4 sts=4 et ai

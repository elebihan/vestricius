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

import os
import argparse
from vestricius import __version__
from vestricius.config import Configuration
from vestricius.presetmanager import PresetManager
from vestricius.pluginmanager import PluginManager
from vestricius.utils import setup_i18n
from vestricius.log import setup_logging, debug
from gettext import gettext as _

setup_i18n()

setup_logging()


class Application:
    """Command line Application"""
    def __init__(self):
        self._preset_mgr = PresetManager()
        self._plugin_mgr = PluginManager()
        self._config = Configuration()

        filename = os.path.expanduser('~/.config/vestricius.conf')
        if os.path.exists(filename):
            self._config.load_from_file(filename)

        for path in self._config.plugins_paths:
            self._plugin_mgr.add_search_path(path)

        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-v', '--version',
                                  action='version',
                                  version=__version__)
        self._parser.add_argument('-P', '--plugins-path',
                                  action='append',
                                  metavar=_('PATH'),
                                  dest='plugins_paths',
                                  default=[],
                                  help=_("set plugins search path"))

        subparsers = self._parser.add_subparsers(dest='command')
        p = subparsers.add_parser('list',
                                  help=_('list available plugins or presets'))
        p.add_argument('-d', '--details',
                       action='store_true',
                       dest='with_details',
                       default=False,
                       help=_("show some details"))
        p.add_argument('object',
                       choices=('plugins', 'presets'),
                       help=_('objects to list'))
        p.set_defaults(func=self._parse_cmd_list)

        p = subparsers.add_parser('add',
                                  help=_('add a new preset for a plugin'))
        p.add_argument('plugin',
                       metavar=_('PLUGIN'),
                       help=_('plugin to use'))
        p.add_argument('preset',
                       metavar=_('PRESET'),
                       help=_('name of the new preset'))
        p.set_defaults(func=self._parse_cmd_add)

        p = subparsers.add_parser('edit',
                                  help=_('edit an existing preset'))
        p.add_argument('preset',
                       metavar=_('NAME'),
                       help=_('preset to edit'))
        p.set_defaults(func=self._parse_cmd_edit)

        p = subparsers.add_parser('remove',
                                  help=_('remove an existing preset'))
        p.add_argument('preset',
                       metavar=_('NAME'),
                       help=_('preset to remove'))
        p.add_argument('-f', '--force',
                       action='store_true',
                       help=_('do not prompt user for confirmation'))
        p.set_defaults(func=self._parse_cmd_remove)

        p = subparsers.add_parser('inspect',
                                  help=_('inspect a crash archive'))
        p.add_argument('filename',
                       metavar=_('FILE'),
                       help=_('path to the crash archive'))
        p.add_argument('-p', '--preset',
                       metavar=_('PRESET'),
                       help=_('name of the preset to use'))
        p.set_defaults(func=self._parse_cmd_inspect)

    def _parse_cmd_list(self, args):
        if args.object == 'presets':
            for preset in self._preset_mgr.presets:
                if args.with_details:
                    text = "{0.name:<24} -- {0.plugin:<48}"
                else:
                    text = "{0.name}"
                print(text.format(preset))
        elif args.object == 'plugins':
            for plugin in self._plugin_mgr.plugins:
                if args.with_details:
                    text = "{0.name:<24} -- {0.description:<48}"
                else:
                    text = "{0.name}"
                print(text.format(plugin))

    def _parse_cmd_add(self, args):
        plugin = self._plugin_mgr.lookup_by_name(args.plugin)
        self._preset_mgr.create(plugin, args.preset)

    def _parse_cmd_edit(self, args):
        self._preset_mgr.edit(args.preset)

    def _parse_cmd_remove(self, args):
        must_remove = False
        if not args.force:
            prompt = _("Do you REALLY want to delete the preset '{}' [y/N]? ")
            value = input(prompt.format(args.preset))
            if value.lower() == _('y'):
                must_remove = True
        else:
            must_remove = True
        if must_remove:
            self._preset_mgr.remove(args.preset)
            print(_("Deleted '{}'").format(args.preset))

    def _parse_cmd_inspect(self, args):
        preset_name = args.preset or self._config.default_preset
        debug(_("Using preset '{}'").format(preset_name))
        preset = self._preset_mgr.lookup_by_name(preset_name)
        plugin = self._plugin_mgr.lookup_by_name(preset.plugin)
        debug(_("Using plugin '{}'").format(plugin.name))
        haruspex = plugin.create_haruspex(preset)
        report = haruspex.inspect(args.filename)
        print(report.format_as_yaml())

    def run(self):
        args = self._parser.parse_args()

        for path in args.plugins_paths:
            self._plugin_mgr.add_search_path(path)

        self._plugin_mgr.scan_plugins()
        self._preset_mgr.scan_presets()

        if not hasattr(args, 'func'):
            self._parser.error(_('Missing command'))
        else:
            args.func(args)


def main():
    app = Application()
    app.run()

# vim: ts=4 sw=4 sts=4 et ai

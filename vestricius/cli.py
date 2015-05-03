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

import argparse
from vestricius import __version__
from vestricius.preset import PresetManager
from vestricius.utils import setup_i18n
from vestricius.log import setup_logging
from gettext import gettext as _

setup_i18n()

setup_logging()


def parse_cmd_list(args):
    if args.object == 'presets':
        manager = PresetManager()
        for preset in manager.presets:
            print(preset.name)


def parse_cmd_new(args):
    manager = PresetManager()
    manager.create(None, args.preset)


def parse_cmd_edit(args):
    manager = PresetManager()
    manager.edit(args.preset)


def parse_cmd_remove(args):
    must_remove = False
    manager = PresetManager()
    if not args.force:
        prompt = _("Do you REALLY want to delete the preset '{}' [y/N]? ")
        value = input(prompt.format(args.preset))
        if value.lower() == _('y'):
            must_remove = True
    else:
        must_remove = True
    if must_remove:
        manager.remove(args.preset)
        print(_("Deleted '{}'").format(args.preset))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version',
                        action='version',
                        version=__version__)
    subparsers = parser.add_subparsers(dest='command')
    p = subparsers.add_parser('list',
                              help=_('list available modules or presets'))
    p.add_argument('object',
                   choices=('modules', 'presets'),
                   help=_('objects to list'))
    p.set_defaults(func=parse_cmd_list)

    p = subparsers.add_parser('new',
                              help=_('create a new preset for a module'))
    p.add_argument('module',
                   metavar=_('NAME'),
                   help=_('module to use'))
    p.add_argument('preset',
                   metavar=_('NAME'),
                   help=_('name of the new preset'))
    p.set_defaults(func=parse_cmd_new)

    p = subparsers.add_parser('edit',
                              help=_('edit an existing preset'))
    p.add_argument('preset',
                   metavar=_('NAME'),
                   help=_('preset to edit'))
    p.set_defaults(func=parse_cmd_edit)

    p = subparsers.add_parser('remove',
                              help=_('remove an existing preset'))
    p.add_argument('preset',
                   metavar=_('NAME'),
                   help=_('preset to remove'))
    p.add_argument('-f', '--force',
                   action='store_true',
                   help=_('do not prompt user for confirmation'))
    p.set_defaults(func=parse_cmd_remove)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.error(_('Missing command'))
    else:
        args.func(args)

# vim: ts=4 sw=4 sts=4 et ai

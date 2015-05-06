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
   vestricius.plugins.test
   ```````````````````````

   Simple Test plugin

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

from vestricius.plugin import Plugin
from vestricius.haruspex import Haruspex
from vestricius.log import info
from gettext import gettext as _


class TestPlugin(Plugin):
    """Test Plugin"""
    def __init__(self):
        pass

    @property
    def name(self):
        return 'test'

    @property
    def description(self):
        return 'Dummy test plugin'

    def create_haruspex(self, preset):
        return TestHaruspex()


class TestHaruspex(Haruspex):
    def __init__(self):
        pass

    def inspect(self, filename):
        info(_("dummy inspection of {}").format(filename))

    def divine(self):
        info(_("dummy divination"))


# vim: ts=4 sw=4 sts=4 et ai

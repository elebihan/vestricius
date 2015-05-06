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
   vestricius.haruspex
   ```````````````````

   Provides basic Haruspex support

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import abc


class Haruspex:
    """Base abstract class for inspecting crash archive.

    This class can not be instanced directly, but must be subclassed.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def inspect(self, filename):
        """Inspects a crash archive.

        @param filename: path to the crash archive file
        @type filename: str
        """
        pass

    @abc.abstractmethod
    def divine(self):
        """Fetches and inspects latest crash archive"""
        pass

# vim: ts=4 sw=4 sts=4 et ai
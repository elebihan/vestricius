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
   vestricius.elf
   ``````````````

   Executable and Linkable Format helpers

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import re
import magic
from .common import InvalidFileError


def extract_executable_path(dumpfile):
    """Extracts executable path from core dump file

    @param dumpfile: path to the core dump file
    @type dumpfile: str
    """
    # TODO: replace with proper ELF parsing
    with magic.Magic() as m:
        desc = m.id_filename(dumpfile)
        fields = [f.strip() for f in desc.split(',')]
        match = re.match(r'from \'(.+)\'', fields[3])
        if match:
            return os.path.basename(match.group(1))
    raise InvalidFileError()

# vim: ts=4 sw=4 sts=4 et ai

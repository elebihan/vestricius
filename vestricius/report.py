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
   vestricius.report
   `````````````````

   Collect and format information from inspection

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import datetime
import pystache


_REPORT_YAML_TEMPLATE = """---
date: {{date}}
filename: {{filename}}
plugin: {{plugin}}
"""


class Report:
    """Collect and format information from inspection.

    @param filename: name of the inspected crash archive
    @type filename: str

    @param plugin: name of plugin used for inspection
    @type plugin: str
    """
    def __init__(self, filename, plugin):
        self._filename = os.path.basename(filename)
        self._plugin = plugin

    @property
    def template(self):
        """Returns the Mustache template of the report"""
        return _REPORT_YAML_TEMPLATE

    @property
    def data(self):
        """Returns the data of the report as a dictionnary"""
        date = datetime.datetime.now()
        data = {
            'date': date.strftime("%Y-%m-%d %H:%M:%S"),
            'filename': self._filename,
            'plugin': self._plugin,
        }
        return data

    def format_as_yaml(self):
        """Returns the report as YAML document.

        @return: the report formatted as YAML
        @rtype: str
        """
        renderer = pystache.Renderer(escape=lambda u: u)
        contents = renderer.render(self.template, self.data)
        return contents

# vim: ts=4 sw=4 sts=4 et ai

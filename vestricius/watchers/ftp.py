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
   vestricius.watchers.ftp
   ```````````````````````

   Provides a watcher for FTP servers

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import time
from ..log import info
from ..fetchers.ftp import FTPFetcher
from ..watcher import Watcher
from gettext import gettext as _


class FTPWatcher(Watcher):
    """Watch for new crash archives dumped on FTP server

    @param url: url of the crash archive repository
    @type url: str

    @param username: optional user name to use for connection
    @type username: str

    @param pasword: optional password
    @type password: str

    @param period: polling period (in seconds)
    @type period: uint16
    """
    def __init__(self, url, username=None, password=None, period=60):
        self._period = period
        self._fetcher = FTPFetcher(url, username, password)

    def watch(self, duration=None, pattern=None, callback=None, data=None):
        handler = lambda f, d, x: info(_("Found '{}' uploaded on {}").format(f, d))
        callback = callback or handler
        elapsed = 0

        msg = _("Checking for new crash archive at {} every {} seconds")
        info(msg.format(self._fetcher.url, self._period))

        latest = self._fetcher.lookup(pattern)
        msg = _("Latest crash archive is '{}', uploaded on {}")
        info(msg.format(latest[0], latest[1]))

        while True:
            time.sleep(self._period)
            results = self._fetcher.lookup(pattern)
            if results:
                result = results[0]
                if latest[0] != result[0]:
                    callback(result[0], result[1], data)
                    latest = result

            elapsed += self._period
            if duration and (elapsed >= duration):
                break

# vim: ts=4 sw=4 sts=4 et ai

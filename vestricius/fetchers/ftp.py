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
   vestricius.fetchers.ftp
   ```````````````````````

   FTP download helper

   :copyright: (C) 2015 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

import os
import re
from ftplib import FTP
from urllib.request import urlretrieve
from urllib.parse import urlparse, urlunparse
from datetime import datetime
from ..log import debug
from ..fetcher import Fetcher
from ..common import FileNotFoundError
from gettext import gettext as _


class FTPFetcher(Fetcher):
    """Fetches crash archive

    @param url: url of the crash archive repository
    @type url: str

    @param username: optional user name to use for connection
    @type username: str

    @param pasword: optional password
    @type password: str
    """
    def __init__(self, url, username=None, password=None):
        parsed_url = urlparse(url)
        self._url = urlunparse((parsed_url.scheme,
                                parsed_url.hostname,
                                parsed_url.path,
                                parsed_url.params,
                                parsed_url.query,
                                parsed_url.fragment))
        self._username = parsed_url.username or username
        self._password = parsed_url.password or password

    @property
    def url(self):
        return self._url

    def _get_url_full(self):
        parsed_url = urlparse(self._url)
        if self._username:
            text = self._username
            if self._password:
                text += ':' + self._password
            text += '@'
        else:
            text = ''
        url = urlunparse((parsed_url.scheme,
                          text + parsed_url.hostname,
                          parsed_url.path,
                          parsed_url.params,
                          parsed_url.query,
                          parsed_url.
                          fragment))
        return url

    def lookup(self, pattern=None):
        debug(_("Looking for crash archive at {}").format(self.url))
        host, path = self._url.strip('ftp://').split('/', 1)
        with FTP(host) as ftp:
            files = []
            ftp.login(self._username, self._password)
            ftp.cwd(path)
            ftp.retrlines('LIST -t .', lambda l: files.append(l.split()[-1]))
            if pattern:
                files = [f for f in files if re.search(pattern, f)]
            if len(files):
                fn = files[0]
                line = ftp.sendcmd("MDTM {}".format(fn))
                code, timestamp = line.split()
                if code == '213':
                    date = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
                else:
                    date = datetime.fromtimestamp(0)
                return (fn, date.strftime("%Y-%m-%d--%H:%M:%S"))
            else:
                raise FileNotFoundError(_("no file found"))

    def fetch(self, pattern=None, dest=None, callback=None):
        fn = self.lookup(pattern)
        return self.retrieve(fn, dest, callback)

    def retrieve(self, filename, dest=None, callback=None):
        dest = dest or os.getcwd()
        path = os.path.join(dest, filename)
        url = self._get_url_full() + filename
        if not os.path.exists(dest):
            os.makedirs(dest)
        (output, headers) = urlretrieve(url, path, callback)
        return output


# vim: ts=4 sw=4 sts=4 et ai

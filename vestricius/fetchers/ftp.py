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
from urllib.parse import urlparse, urlunparse
from ..common import ProgressReporter


class FtpFetcher:
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

    def lookup(self, pattern=None):
        print("Searching for crash archive at {}".format(self._url))
        host, path = self._url.strip('ftp://').split('/', 1)
        with FTP(host) as ftp:
            files = []
            ftp.login(self._username, self._password)
            ftp.cwd(path)
            ftp.retrlines('LIST -t .', lambda l: files.append(l.split()[-1]))
            if pattern:
                files = [f for f in files if re.search(pattern, f)]
            if len(files):
                return files[0]
            else:
                raise FileNotFoundError

    def fetch(self, pattern=None, dest=os.getcwd(), callback=None):
        fn = self.lookup(pattern)
        return self.retrieve(fn, dest, callback)

    def retrieve(self, filename, dest=os.getcwd(), callback=None):
        host, path = self._url.strip('ftp://').split('/', 1)
        output = os.path.join(dest, filename)
        if not os.path.exists(dest):
            os.makedirs(dest)
        with FTP(host) as ftp:
            ftp.login(self._username, self._password)
            ftp.cwd(path)
            size = ftp.size(filename)
            r = ProgressReporter(filename, output, size, callback)
            with open(output, 'wb') as f:
                def write_chunk(chunk):
                    f.write(chunk)
                    r.update(len(chunk))
                ftp.retrbinary('RETR ' + filename, write_chunk)
        return output


# vim: ts=4 sw=4 sts=4 et ai

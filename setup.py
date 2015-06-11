#!/usr/bin/env python3
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

from setuptools import setup, find_packages
from disthelpers import extract_messages, init_catalog, update_catalog
from disthelpers import build, build_catalog, build_man
from glob import glob
import vestricius

setup(name='vestricius',
      version=vestricius.__version__,
      description='Inspect crash archives',
      long_description='''
      Vestricius is an Haruspex, a priest who practiced divination by
      looking at the entrails of animals. `vestricius(1)` is a command line
      tool which allows the user to get a backtrace from a core dump file.
      ''',
      license='GPLv3+',
      url='https://github.com/elebihan/vestricius/',
      platforms=['Any'],
      keywords=[],
      install_requires=[
          'colorama>=0.3',
          'pyelftools>=0.23',
          'pystache>=0.5.4',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
      ],
      packages=find_packages(),
      data_files=[
          ('share/zsh/site-functions', glob('shell-completion/zsh/_*')),
      ],
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'vestricius = vestricius.cli:main',
          ],
      },
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      cmdclass={'build': build,
                'build_man': build_man,
                'extract_messages': extract_messages,
                'init_catalog': init_catalog,
                'update_catalog': update_catalog,
                'build_catalog': build_catalog})

# vim: ts=4 sts=4 sw=4 sta et ai

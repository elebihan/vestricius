===============
vestricius.conf
===============

---------------------------------
Configuration file for Vestricius
---------------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2015 Eric Le Bihan
:Manual section: 5

DESCRIPTION
===========

The ``vestricius.conf`` file contains the configuration parameters for
`vestricius(1)`. It uses a structure similar to Microsoft Windows INI files.

The default location for this file is ``~/.config/vestricius.conf``.

SYNTAX
======

The file contains sections, led by a *[section]* header followed by
*key=value* pairs. Lines beginning with '#' are considered as comments.

Example::

  # Configuration file
  [General]
  DefaultPreset = simple-core
  DefaultPlugin = capsula

SECTIONS
========

Here is the list of potential sections.

General
-------

* DefaultPreset: the default preset to use
* DefaultPlugin: the default plugin to use
* PluginsPaths: comma separated list of paths to additional plugins

SEE ALSO
========

- ``vestricius(1)``

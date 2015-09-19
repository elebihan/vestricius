===================
vestricius-tutorial
===================

-------------------------------------
A tutorial introduction to Vestricius
-------------------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2015 Eric Le Bihan
:Manual section: 7

COOKBOOK
========

To create a new preset named "foo" for plugin "simple-core", use the command
"add"::

  $ vestricius add simple-core foo

The default editor configured will be summoned to customize the preset with
parameters such as the path to the debugger to use to generate the backtrace or
the path to the unstripped binaries.

To edit the preset again, use the "edit" command::

  $ vestricius edit foo

To inspect a core dump using this preset, use the "inspect" command::

  $ vestricius inspect --preset foo /path/to/crash/archive

A crash archive may be stored on a repository, such as a FTP server. If the URL
of the repository is set in the preset file, `vestricius(1)` can look for the
latest crash archive via the command "peek"::

  $ vestricius peek --preset foo

To automatically retrieve and inspect this archive, use the command "reveal"::

  $ vestricius reveal --preset foo

It is possible to set a default preset to use for all the operation, thus
avoiding to use *--preset*. See `vestricius.conf(5)` for details.

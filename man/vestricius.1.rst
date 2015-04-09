==========
vestricius
==========

----------------------
Inspect crash archives
----------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2015 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

vestricius [OPTIONS] <command> [<argument>, ...]

vestricius new <module> <preset>

vestricius list <modules|presets>

vestricius edit <preset>

DESCRIPTION
===========

Vestricius is an Haruspex, a priest who practiced divination by
looking at the entrails of animals. `vestricius(1)` is a command line
tool which allows the user to get a backtrace from a core dump file.

OPTIONS
=======

-v, --version   display program version and exit

COMMANDS
========

The following commands are available:

list [OPTIONS] <modules|presets>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List the available modules or presets.

new [OPTIONS] <module> <preset>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new preset for an existing module.

edit [OPTIONS] <preset>
~~~~~~~~~~~~~~~~~~~~~~~

Edit an existing preset.

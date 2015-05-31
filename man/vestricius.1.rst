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

vestricius add <plugin> <preset>

vestricius list <plugins|presets>

vestricius edit <preset>

vestricius inspect <filename>

vestricius peek

vestricius reveal

Vestricius is an Haruspex, a priest who practiced divination by
looking at the entrails of animals. `vestricius(1)` is a command line
tool which allows the user to get a backtrace from a core dump file.

OPTIONS
=======

-v, --version                    display program version and exit
-P PATH, --plugins-path=PATH     set plugins search path

COMMANDS
========

The following commands are available:

list [OPTIONS] <modules|presets>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List the available modules or presets.

add [OPTIONS] <module> <preset>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new preset for an existing module.

edit [OPTIONS] <preset>
~~~~~~~~~~~~~~~~~~~~~~~

Edit an existing preset.

inspect [OPTIONS] <filename>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inspect a crash archive.

Available options:

-p PRESET, --preset=PRESET    name of the preset to use
-o FILE, --output=FILE        set output filename

peek [OPTIONS]
~~~~~~~~~~~~~~

Show information about the latest crash archive

Available options:

-p PRESET, --preset=PRESET    name of the preset to use
-P EXPR, --pattern=EXPR       pattern of crash archive name

reveal [OPTIONS]
~~~~~~~~~~~~~~~~

Fetch and inspect the latest crash archive.

Available options:

-p PRESET, --preset=PRESET    name of the preset to use
-o FILE, --output=FILE        set output filename
-P EXPR, --pattern=EXPR       pattern of crash archive name

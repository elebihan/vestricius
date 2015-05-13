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

from elftools.elf.elffile import ELFFile
from elftools.elf.segments import NoteSegment
from elftools.common.utils import roundup, struct_parse
from elftools.elf.structs import Enum, Struct, ULInt32, UBInt8
from elftools.construct import CString, Pass, StaticField
from .common import InvalidFileError


_GNU_NOTE_TYPES = dict(NT_PRSTATUS=1,
                       NT_FPRREGSET=2,
                       NT_PRPSINFO=3,
                       NT_TASKSTRUCT=4,
                       NT_PLATFORM=5,
                       NT_AUXV=6,
                       _default_=Pass)


def iter_notes(segment):
    offset = segment['p_offset']
    end = offset + segment['p_filesz']
    segment.stream.seek(offset)
    while offset < end:
        nhdr = Struct('Elf_Nhdr',
                      ULInt32('n_namesz'),
                      ULInt32('n_descsz'),
                      Enum(ULInt32('n_type'), **_GNU_NOTE_TYPES))
        note = struct_parse(nhdr, segment.stream, offset)
        note['n_offset'] = offset
        offset += nhdr.sizeof()
        segment.stream.seek(offset)
        size = roundup(note['n_namesz'], 2)
        data = CString('').parse(segment.stream.read(size))
        note['n_name'] = data.decode('latin-1')
        offset += size
        note['n_desc'] = segment.stream.read(note['n_descsz'])
        offset += roundup(note['n_descsz'], 2)
        note['n_size'] = offset - note['n_offset']
        yield note


def parse_note(note):
    prpsinfo = Struct('elf_psinfo',
                      UBInt8('pr_state'),
                      UBInt8('pr_sname'),
                      UBInt8('pr_zomb'),
                      UBInt8('pr_nice'),
                      ULInt32('pr_flag'),
                      ULInt32('pr_uid'),
                      ULInt32('pr_gid'),
                      ULInt32('pr_pid'),
                      ULInt32('pr_ppid'),
                      ULInt32('pr_pgrp'),
                      ULInt32('pr_sid'),
                      StaticField('pr_fname', 16),
                      StaticField('pr_psargs', 80))
    psinfo = prpsinfo.parse(note['n_desc'])
    fname = CString('').parse(psinfo['pr_fname']).decode('latin-1')
    psargs = CString('').parse(psinfo['pr_psargs']).decode('latin-1')
    return (fname, psargs)


def extract_executable_path(dumpfile):
    """Extracts executable path from core dump file

    @param dumpfile: path to the core dump file
    @type dumpfile: str
    """
    with open(dumpfile, 'rb') as f:
        elffile = ELFFile(f)
        for segment in elffile.iter_segments():
            if isinstance(segment, NoteSegment):
                for note in iter_notes(segment):
                    if (note['n_name'] == 'CORE' and
                        note['n_type'] == 'NT_PRPSINFO'):
                        fname, psargs = parse_note(note)
                        return fname
    raise InvalidFileError

# vim: ts=4 sw=4 sts=4 et ai

#! /usr/bin/env python

# Copyright (C) 2012-2014  SeaGoatVision - http://seagoatvision.org
#
# This file is part of SeaGoatVision.
#
# SeaGoatVision is free software: you can redistribute it and/or modify
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from seagoatvision.server.cpp.create_module import *
import os

# PYTHON FILTERS IMPORT
for f in os.listdir(os.path.dirname(__file__)):
    if not f.endswith(".py") or f == "__init__.py":
        continue
    filename, _ = os.path.splitext(f)
    code = 'from .%(module)s import *' % {'module': filename}
    exec(code)

# Global variable for cpp filter
# TODO find another solution to remove global variable, like log file
if 'cppfiles' not in globals():
    global cppfiles
    cppfiles = {}
if 'cpptimestamps' not in globals():
    global cpptimestamps
    cpptimestamps = {}

# C++ FILTERS IMPORT
import_all_cpp_filter(cppfiles, cpptimestamps, sys.modules[__name__], __file__)

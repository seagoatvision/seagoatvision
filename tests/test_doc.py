#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
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

from subprocess import STDOUT, check_output as qx
from subprocess import CalledProcessError
import unittest2

CMD_GENERATE_DOC = "make SPHINXOPTS='-q' -C ./doc html"
CMD_DOCTEST = "python2 -m doctest -v SeaGoatVision/commons/param.py"
# TIMEOUT_DOC = 60


class TestDoc(unittest2.TestCase):
    def test_generate_doc(self):
        """
        Generate documentation and search warning or error message.
        """
        # TODO implement a timeout. works in python3.4
        # output = qx(CMD_GENERATE_DOC, stderr=STDOUT, shell=True,
        # timeout=TIMEOUT_DOC).decode('utf8')
        try:
            output = qx(CMD_GENERATE_DOC, stderr=STDOUT, shell=True).decode(
                'utf8')
        except CalledProcessError as e:
            print(e.output)
            raise
        print(output)
        # Exception, remove the warning of coverage no data collected
        rem_warn = "Coverage.py warning: No data was collected."
        out = output.replace(rem_warn, "").upper()
        assert "WARNING" not in out
        assert "ERROR" not in out

    def test_doctest(self):
        """
        Start doctest and search warning or error message
        """
        try:
            output = qx(CMD_DOCTEST, stderr=STDOUT, shell=True).decode('utf8')
        except CalledProcessError as e:
            print(e.output)
            raise
        print(output)
        out = output.upper()
        assert "WARNING" not in out
        assert "ERROR" not in out

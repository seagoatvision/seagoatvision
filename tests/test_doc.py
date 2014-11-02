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

import common_test_tools as ctt
from subprocess import STDOUT, check_output as qx
from subprocess import CalledProcessError
import unittest2

LST_IGNORE_WARNING = ctt.LST_IGNORE_WARNING

CMD_GENERATE_DOC = "make SPHINXOPTS='-q' -C ./doc html"
CMD_DOCTEST = "python2 -m doctest -v seagoatvision/commons/param.py"
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
            self.fail(e)
        try:
            ctt.expect_warning_str(output)
        except BaseException as e:
            self.fail(e)

    def test_doctest(self):
        """
        Start doctest and search warning or error message
        """
        try:
            output = qx(CMD_DOCTEST, stderr=STDOUT, shell=True).decode('utf8')
        except CalledProcessError as e:
            print(e.output)
            self.fail(e)
        try:
            ctt.expect_warning_str(output)
        except BaseException as e:
            self.fail(e)

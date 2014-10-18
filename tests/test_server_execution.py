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

import pexpect
import common_test_tools as ctt
import unittest2

DELAY_START_SERVER = ctt.DELAY_START_SERVER
DELAY_CLOSE_SERVER = ctt.DELAY_CLOSE_SERVER
SERVER_PATH = ctt.SERVER_PATH
SERVER_START_STR = ctt.SERVER_START_STR
SERVER_START_DUPLICATE_STR = ctt.SERVER_START_DUPLICATE_STR


class TestStartServer(unittest2.TestCase):
    def test_run_and_stop_server(self):
        """
        The test will start and stop the server
        """
        total_delay_life_sgv = DELAY_START_SERVER + DELAY_CLOSE_SERVER * 2
        child = ctt.start_server(timeout=total_delay_life_sgv)

        ctt.stop_server(child)

    def test_double_open_server(self):
        total_delay_life_sgv = DELAY_START_SERVER + DELAY_CLOSE_SERVER * 2
        child_1 = ctt.start_server(timeout=total_delay_life_sgv)

        child_2 = pexpect.spawn(SERVER_PATH, timeout=DELAY_START_SERVER)
        str_attempt = SERVER_START_DUPLICATE_STR
        str_not_attempt = SERVER_PATH
        ctt.expect(child_2, str_attempt, not_expect_value=str_not_attempt,
                   timeout=DELAY_START_SERVER)

        ctt.stop_server(child_1)

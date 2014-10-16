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
import common_test_tools

SERVER_PATH = common_test_tools.SERVER_PATH
CLIENT_PATH = common_test_tools.CLIENT_PATH
DELAY_START_SERVER = common_test_tools.DELAY_START_SERVER
DELAY_CLOSE_SERVER = common_test_tools.DELAY_CLOSE_SERVER
DELAY_START_CLI = common_test_tools.DELAY_START_CLI


def test_is_not_connected_cli():
    """
    Start the client cli and check if not connected.
    :return:
    """
    child = pexpect.spawn(CLIENT_PATH + " cli", timeout=DELAY_START_CLI)
    str_attempt = "Connection refused"
    common_test_tools.expect(child, str_attempt, DELAY_START_CLI)


def test_is_connected_cli():
    """
    Start the client cli and check if connected.
    :return:
    """
    # server = _run_server()
    # client = _run_cli()
    pass

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

import psutil
import pexpect
import common_test_tools

SERVER_PATH = common_test_tools.SERVER_PATH
CLIENT_PATH = common_test_tools.CLIENT_PATH
DELAY_START_SERVER = common_test_tools.DELAY_START_SERVER
DELAY_CLOSE_SERVER = common_test_tools.DELAY_CLOSE_SERVER
DELAY_START_CLI = common_test_tools.DELAY_START_CLI


def test_run_and_stop_server():
    """
    The test will start and stop the server
    """
    total_delay_life_sgv = DELAY_START_SERVER + DELAY_CLOSE_SERVER * 2
    child = pexpect.spawn(SERVER_PATH, timeout=total_delay_life_sgv)
    str_attempt = "Waiting command"
    common_test_tools.expect(child, str_attempt, DELAY_START_SERVER)

    # server is running. Send a sigterm
    p = psutil.Process(child.pid)
    child.terminate()
    str_attempt = "Close SeaGoat. See you later!"
    common_test_tools.expect(child, str_attempt, DELAY_CLOSE_SERVER)

    # be sure it's close
    assert p
    # print(p.status())
    try:
        status = p.wait(DELAY_CLOSE_SERVER)
        # test if status is sigterm
        assert not status
    except psutil.TimeoutExpired:
        p.kill()
        raise

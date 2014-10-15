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

SERVER_PATH = '../server.py'
CLIENT_PATH = '../client.py'


def test_run_and_stop_server():
    """
    The test will start and stop the server
    """
    child = pexpect.spawn(SERVER_PATH, timeout=20)
    str_attempt = "Waiting command"
    _expect(child, str_attempt, 5)

    # server is running. Send a sigterm
    p = psutil.Process(child.pid)
    child.terminate()
    str_attempt = "Close SeaGoat. See you later!"
    _expect(child, str_attempt, 3)

    # be sure it's close
    assert p
    # print(p.status())
    try:
        status = p.wait(3)
        # test if status is sigterm
        assert not status
    except psutil.TimeoutExpired:
        p.kill()
        raise


def test_is_not_connected_cli():
    """
    Start the client cli and check if not connected.
    :return:
    """
    child = pexpect.spawn(CLIENT_PATH + " cli", timeout=3)
    str_attempt = "Connection refused"
    _expect(child, str_attempt, 3)


def test_is_connected_cli():
    """
    Start the client cli and check if connected.
    :return:
    """
    # server = _run_server()
    # client = _run_cli()
    pass


def _expect(child, str_attempt, timeout):
    expected = [str_attempt, pexpect.EOF, pexpect.TIMEOUT]
    index = child.expect(expected, timeout=timeout)
    if index:
        print(child.before)
        if index == 1:
            print("Process is finished")
        else:
            print("Cannot find str %s" % str_attempt)
    assert not index

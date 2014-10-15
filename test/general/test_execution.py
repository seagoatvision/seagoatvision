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

import subprocess
import psutil
import pexpect

SERVER_PATH = '../server.py'
CLIENT_PATH = '../client.py'


def test_run_and_stop_server():
    """
    The test will start and stop the server
    """
    subp = _run_server()
    assert _kill_server(subp, timeout=5)


def test_is_not_connected_cli():
    """
    Start the client cli and check if not connected.
    :return:
    """
    child = pexpect.spawn(CLIENT_PATH + " cli", timeout=3)
    str_attempt = "Connection refused"
    expected = [str_attempt, pexpect.EOF, pexpect.TIMEOUT]
    index = child.expect(expected, timeout=2)
    # print(child.before)
    assert not index


def _run_server():
    """
    Execute a process
    :return: subprocess of server.py
    """
    return subprocess.Popen([SERVER_PATH])


def _kill_server(subp, timeout=0):
    """
    Kill the server with a timeout
    :param supb: subprocess of the server
    :param timeout: second from creation to wait to kill the process.
    :return: success
    """
    delay_terminate = 3
    assert subp
    p = psutil.Process(subp.pid)
    assert p
    try:
        print("Waiting max %s seconds to kill %s" % (timeout, SERVER_PATH))
        status = p.wait(timeout)
        raise Exception("Process already stopped - return code %s" % status)
    except psutil.TimeoutExpired:
        print("terminate")
        p.terminate()
    # test if really terminate
    try:
        status = p.wait(delay_terminate)
        # test if status is sigterm
        assert status == 15
    except psutil.TimeoutExpired:
        p.kill()
        raise
    return True

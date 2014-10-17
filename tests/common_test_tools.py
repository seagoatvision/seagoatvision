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

SERVER_PATH = './server.py'
CLIENT_PATH = './client.py'
DELAY_START_SERVER = 30
DELAY_CLOSE_SERVER = 10
DELAY_START_CLI = 3


def start_server(timeout=0):
    """

    :param timeout: timeout to kill server
    :return: spawn process of server
    """
    child = pexpect.spawn(SERVER_PATH, timeout=timeout)
    str_attempt = "Waiting command"
    expect(child, str_attempt, DELAY_START_SERVER)
    return child


def stop_server(child):
    """

    :param child:
    """
    p = psutil.Process(child.pid)
    child.terminate()
    str_attempt = "Close SeaGoat. See you later!"
    expect(child, str_attempt, DELAY_CLOSE_SERVER)

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


def expect(child, str_attempt, timeout):
    """
    Use pexpect.expect and print the execution if not expected.
    :param child: pexpect child
    :param str_attempt: searching str in execution
    :param timeout: limit of time to expect the string
    """
    expected = [str_attempt, pexpect.EOF, pexpect.TIMEOUT]
    index = child.expect(expected, timeout=timeout)
    if index:
        print(child.before)
        if index == 1:
            print("Error, process is already close, receive pexpect.OEF.")
        else:
            print("Cannot find expected str : %s" % str_attempt)
    assert not index

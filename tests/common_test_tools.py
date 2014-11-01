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

import psutil
import pexpect
import sys

SERVER_PATH = './server.py'
CLIENT_PATH = './client.py'
DELAY_START_SERVER = 30
DELAY_CLOSE_SERVER = 10
DELAY_START_CLI = 10
SERVER_START_STR = "Waiting command"
SERVER_START_DUPLICATE_STR = "SeaGoat already run with the pid"
SERVER_CLOSE_STR = "Close SeaGoat. See you later!"
CLI_CMD_READY = "(Cmd)"
LST_IGNORE_WARNING = ["Coverage.py warning: No data was collected.",
                      "libdc1394 error: Failed to initialize libdc1394",
                      "Camera Webcam not detected"]


def start_server(timeout=0, verbose=False):
    """

    :param timeout: timeout to kill server
    :param verbose: write output of child in sys.stdout
    :return: spawn process of server
    """
    child = pexpect.spawn(SERVER_PATH, timeout=timeout)
    if verbose:
        child.logfile_read = sys.stdout
    str_attempt = "Waiting command"
    str_not_attempt = SERVER_START_DUPLICATE_STR
    expect(child, str_attempt, not_expect_value=str_not_attempt,
           timeout=DELAY_START_SERVER)
    # print("Start server pid %s" % child.pid)
    return child


def start_cli(cmd, timeout=0, verbose=False):
    child = pexpect.spawn(cmd, timeout=timeout)
    if verbose:
        child.logfile_read = sys.stdout
    str_attempt = CLI_CMD_READY
    expect(child, str_attempt, timeout=DELAY_START_CLI)
    return child


def stop_server(child):
    p = psutil.Process(child.pid)
    # print("Stop server pid %s" % child.pid)
    # be sure it's close
    if not p:
        raise BaseException("Process is None")
    if not p.is_running():
        raise BaseException("Process is not running.")

    child.terminate()
    expect(child, SERVER_CLOSE_STR, timeout=DELAY_CLOSE_SERVER)

    try:
        status = p.wait(DELAY_CLOSE_SERVER)
        if status:
            raise BaseException(
                "Server wasn't kill with SIGINT or didn't close normally, \
                signal %s." % status)
    except psutil.TimeoutExpired:
        p.kill()
        raise psutil.TimeoutExpired


def expect_warning_str(data):
    print(data)
    ori_data = data.splitlines()
    lines = data.upper().splitlines()
    error = []
    i = 0
    for line in lines:
        ori_line = ori_data[i]
        for str_ignore in LST_IGNORE_WARNING:
            if str_ignore in ori_line:
                break
        else:
            if "WARNING" in line or "ERROR" in line:
                error.append(ori_line)
        i += 1
    if error:
        raise BaseException(error)


def expect(child, expect_value, not_expect_value=None, timeout=0):
    """
    Use pexpect.expect and print the execution if not expected.
    :param child: pexpect child
    :param str_attempt: searching str in execution
    :param timeout: limit of time to expect the string
    """
    msg_err_wrong_param = "Param %s need to be a str or list."
    fail_msg = "Receive \"%s\" and expected \"%s\". Debug %s Index %s."
    expected = [pexpect.EOF, pexpect.TIMEOUT]

    if not expect_value:
        raise BaseException("Param expect_value is empty.")
    elif type(expect_value) is str \
            or expect_value is pexpect.EOF \
            or expect_value is pexpect.TIMEOUT:
        expect_value = [expect_value]
    elif type(expect_value) is not list:
        raise BaseException(msg_err_wrong_param % "expect_value")

    expected_index = range(len(expected), len(expected) + len(expect_value))
    expected += expect_value

    if not_expect_value:
        if type(not_expect_value) is str:
            not_expect_value = [not_expect_value]
        elif type(not_expect_value) is not list:
            raise BaseException(msg_err_wrong_param % "not_expect_value")
        expected += not_expect_value

    index = child.expect(expected, timeout=timeout)
    # Error if not inside the expected index
    if index not in expected_index:
        print("\n############################################################")
        print("\nDebug index %s, expected value %s, pass expected %s, "
              "expected index %s\n" % (
                  index, expected, expect_value, expected_index))
        print(child.before)
        print(child.after)
        print("\n############################################################")
        val = expect_value[0] if len(expect_value) == 1 else expect_value
        raise BaseException(fail_msg % (expected[index], val, expected, index))
        # print expected

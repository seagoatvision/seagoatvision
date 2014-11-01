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

import pexpect
import common_test_tools as ctt
import unittest2
import signal
import os

DELAY_START_SERVER = ctt.DELAY_START_SERVER
DELAY_CLOSE_SERVER = ctt.DELAY_CLOSE_SERVER
SERVER_PATH = ctt.SERVER_PATH
SERVER_START_STR = ctt.SERVER_START_STR
SERVER_START_DUPLICATE_STR = ctt.SERVER_START_DUPLICATE_STR
SERVER_START_CORRUPTED_LOCK = "SeaGoat lock is corrupted"
LOCK_FILE = "/tmp/SeaGoat.lock"


class TestStartServer(unittest2.TestCase):
    def tearDown(self):
        # kill server
        os.system("ps -C 'python2.7 ./server' -o pid=|xargs -r kill -9")
        os.system("rm -f %s" % LOCK_FILE)

    def test_run_and_stop_server(self):
        """
        The test will start and stop the server
        """
        total_delay_life_sgv = DELAY_START_SERVER + DELAY_CLOSE_SERVER * 2
        try:
            child = ctt.start_server(timeout=total_delay_life_sgv)
        except BaseException as e:
            self.fail(e)

        try:
            ctt.stop_server(child)
        except BaseException as e:
            self.fail(e)

    def test_double_open_server(self):
        total_delay_life_sgv = DELAY_START_SERVER + DELAY_CLOSE_SERVER * 2
        try:
            child_1 = ctt.start_server(timeout=total_delay_life_sgv)

            child_2 = pexpect.spawn(SERVER_PATH, timeout=DELAY_START_SERVER)
            str_attempt = SERVER_START_DUPLICATE_STR
            str_not_attempt = SERVER_START_STR
            ctt.expect(child_2, str_attempt, not_expect_value=str_not_attempt,
                       timeout=DELAY_START_SERVER)
            ctt.expect(child_2, pexpect.EOF, timeout=DELAY_CLOSE_SERVER)
            ctt.stop_server(child_1)
        except BaseException as e:
            self.fail(e)

    def test_false_lock_open_server(self):
        try:
            total_delay_life_sgv = DELAY_START_SERVER + DELAY_CLOSE_SERVER * 2
            child_1 = ctt.start_server(timeout=total_delay_life_sgv)
            # force kill it and lock will stay here
            child_1.kill(signal.SIGKILL)
            child_1.wait()

            child_2 = pexpect.spawn(SERVER_PATH, timeout=DELAY_START_SERVER)
            str_attempt = SERVER_START_STR
            str_not_attempt = SERVER_START_DUPLICATE_STR
            ctt.expect(child_2, str_attempt, not_expect_value=str_not_attempt,
                       timeout=DELAY_START_SERVER)

            ctt.stop_server(child_2)
        except BaseException as e:
            self.fail(e)

    def test_open_server_corrupted_lock(self):
        try:
            os.system("echo 'patate' > %s" % LOCK_FILE)

            child = pexpect.spawn(SERVER_PATH, timeout=DELAY_START_SERVER)
            str_attempt = SERVER_START_CORRUPTED_LOCK
            str_not_attempt = SERVER_START_STR
            ctt.expect(child, str_attempt, not_expect_value=str_not_attempt,
                       timeout=DELAY_START_SERVER)
            ctt.expect(child, pexpect.EOF, timeout=DELAY_CLOSE_SERVER)

            os.remove(LOCK_FILE)
        except BaseException as e:
            self.fail(e)

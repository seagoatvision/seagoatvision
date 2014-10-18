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

SERVER_PATH = ctt.SERVER_PATH
CLIENT_CLI_PATH = ctt.CLIENT_PATH + " cli"
DELAY_START_SERVER = ctt.DELAY_START_SERVER
DELAY_CLOSE_SERVER = ctt.DELAY_CLOSE_SERVER
DELAY_START_CLI = ctt.DELAY_START_CLI
CLI_CONNECTED_MSG = "You are connected."
CLI_DISCONNECTED_MSG = "You are disconnected."
SERVER_RECEIVE_CMD = "Request : %s"


# TODO test with local and remote!
class TestCliNotConnected(unittest2.TestCase):
    def test_is_not_connected(self):
        """
        Start the client cli and check if not connected.
        :return:
        """
        child = pexpect.spawn(CLIENT_CLI_PATH, timeout=DELAY_START_CLI)
        str_attempt = "Connection refused"
        ctt.expect(child, str_attempt, timeout=DELAY_START_CLI)

    def test_is_disconnected(self):
        total_delay_life_sgv = DELAY_START_SERVER + DELAY_CLOSE_SERVER * 2
        child_srv = ctt.start_server(timeout=total_delay_life_sgv)
        child_cli = pexpect.spawn(CLIENT_CLI_PATH, timeout=DELAY_START_CLI)

        # Test is connected
        cmd = "is_connected"
        str_attempt_cli = CLI_CONNECTED_MSG
        str_attempt_srv = SERVER_RECEIVE_CMD % cmd
        child_cli.sendline(cmd)
        ctt.expect(child_cli, str_attempt_cli, timeout=DELAY_START_CLI)
        ctt.expect(child_srv, str_attempt_srv, timeout=DELAY_START_CLI)

        ctt.stop_server(child_srv)

        # test is disconnected
        cmd = "is_connected"
        str_attempt_cli = CLI_DISCONNECTED_MSG
        child_cli.sendline(cmd)
        ctt.expect(child_cli, str_attempt_cli, timeout=DELAY_START_CLI)

        # test is connected
        child_srv = ctt.start_server(timeout=total_delay_life_sgv)
        str_attempt_cli = CLI_CONNECTED_MSG
        str_attempt_srv = SERVER_RECEIVE_CMD % cmd
        child_cli.sendline(cmd)
        ctt.expect(child_cli, str_attempt_cli, timeout=DELAY_START_CLI)
        ctt.expect(child_srv, str_attempt_srv, timeout=DELAY_START_CLI)

        ctt.stop_server(child_srv)


class TestCli(unittest2.TestCase):
    """
    Test functionality of all command in cli
    """
    # TODO test autocomplete in cli
    # TODO the cli is suppose to receive real with no other comment
    # TODO remove "Nombre de ligne"
    # TODO test when close server before closing cli (or sending new command)
    @classmethod
    def setUpClass(cls):
        # 15 minutes, it's enough for all command test
        total_delay_life_sgv = 60 * 15
        cls._srv = ctt.start_server(timeout=total_delay_life_sgv)

        # open client
        child = pexpect.spawn(CLIENT_CLI_PATH, timeout=DELAY_START_CLI)
        str_attempt = "(Cmd)"
        ctt.expect(child, str_attempt, timeout=DELAY_START_CLI)
        cls._cli = child

    @classmethod
    def tearDownClass(cls):
        ctt.stop_server(cls._srv)

    def test_is_connected(self):
        cmd = "is_connected"
        str_attempt_cli = CLI_CONNECTED_MSG
        str_attempt_srv = SERVER_RECEIVE_CMD % cmd
        self._cli.sendline(cmd)
        ctt.expect(self._cli, str_attempt_cli, timeout=DELAY_START_CLI)
        ctt.expect(self._srv, str_attempt_srv, timeout=DELAY_START_CLI)

    def test_get_media_list(self):
        cmd = "get_media_list"
        # attempt at minimum the media File
        str_attempt_cli = "File"
        str_attempt_srv = SERVER_RECEIVE_CMD % cmd
        self._cli.sendline(cmd)
        ctt.expect(self._cli, str_attempt_cli, timeout=DELAY_START_CLI)
        ctt.expect(self._srv, str_attempt_srv, timeout=DELAY_START_CLI)

    def test_zzz_exit(self):
        # IMPORTANT, this test need to be executed at the end
        cmd = "exit"
        # exit not exist in the server, attempt a message that precise we
        # cannot close the remote server
        # TODO validate the server has no more print and receive a timeout
        str_attempt_cli = "Cannot close remote server."
        # str_attempt_srv = SERVER_RECEIVE_CMD % cmd
        self._cli.sendline(cmd)
        ctt.expect(self._cli, str_attempt_cli, timeout=DELAY_START_CLI)
        # ctt.expect(self._srv, str_attempt_srv, timeout=DELAY_START_CLI)

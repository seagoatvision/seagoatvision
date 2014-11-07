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
from seagoatvision.server.core.configuration import Configuration

SERVER_PATH = ctt.SERVER_PATH
CLIENT_CLI_PATH = ctt.CLIENT_PATH + " cli"
CLIENT_CLI_LOCAL_PATH = ctt.CLIENT_PATH + " cli --local"
DELAY_START_SERVER = ctt.DELAY_START_SERVER
DELAY_CLOSE_SERVER = ctt.DELAY_CLOSE_SERVER
DELAY_START_CLI = ctt.DELAY_START_CLI
SERVER_RECEIVE_CMD = "Request : %s"

CLI_EXPECT_CONNECTED = "You are connected."
CLI_EXPECT_DISCONNECTED = "You are disconnected."
CLI_EXPECT_GET_MEDIA_LIST = "generator"
CLI_EXPECT_GET_FILTER_LIST = "YUV2BGR"
CLI_EXPECT_GET_FILTERCHAIN_LIST = "Example"
CLI_EXPECT_EXIT = "Cannot close remote server."

EXECUTION_NAME_EXAMPLE = "Example"

conf = Configuration()


class TestCliNotConnected(unittest2.TestCase):
    def test_is_not_connected(self):
        """
        Start the client cli and check if not connected.
        :return:
        """
        child = pexpect.spawn(CLIENT_CLI_PATH, timeout=DELAY_START_CLI)
        str_attempt = "Connection refused"
        try:
            ctt.expect(child, str_attempt, timeout=DELAY_START_CLI)
        except BaseException as e:
            self.fail(e)

    def test_is_disconnected(self):
        try:
            total_delay_life_sgv = DELAY_START_SERVER + DELAY_CLOSE_SERVER * 2
            child_srv = ctt.start_server(timeout=total_delay_life_sgv)
            child_cli = pexpect.spawn(CLIENT_CLI_PATH, timeout=DELAY_START_CLI)

            # Test is connected
            cmd = "is_connected"
            str_attempt_cli = CLI_EXPECT_CONNECTED
            str_attempt_srv = SERVER_RECEIVE_CMD % cmd
            child_cli.sendline(cmd)
            ctt.expect(child_cli, str_attempt_cli, timeout=DELAY_START_CLI)
            ctt.expect(child_srv, str_attempt_srv, timeout=DELAY_START_CLI)

            ctt.stop_server(child_srv)

            # test is disconnected
            lst_cmd = ["get_media_list", "stop_record", "start_record",
                       "stop_filterchain_execution",
                       "start_filterchain_execution",
                       "stop_output_observer", "add_output_observer",
                       "get_filterchain_list", "get_filter_list",
                       "is_connected"]
            for cmd in lst_cmd:
                str_attempt_cli = CLI_EXPECT_DISCONNECTED
                child_cli.sendline(cmd + " test")
                ctt.expect(child_cli, str_attempt_cli, timeout=DELAY_START_CLI)

            # test is connected
            child_srv = ctt.start_server(timeout=total_delay_life_sgv)
            str_attempt_cli = CLI_EXPECT_CONNECTED
            str_attempt_srv = SERVER_RECEIVE_CMD % cmd
            child_cli.sendline(cmd)
            ctt.expect(child_cli, str_attempt_cli, timeout=DELAY_START_CLI)
            ctt.expect(child_srv, str_attempt_srv, timeout=DELAY_START_CLI)

            ctt.stop_server(child_srv)
        except BaseException as e:
            self.fail(e)


class TestCli(unittest2.TestCase):
    """
    Test functionality of all command in cli
    """

    @classmethod
    def setUpClass(cls):
        # 5 minutes, it's enough for all command test
        total_delay_life_sgv = 60 * 5
        cls._srv = ctt.start_server(timeout=total_delay_life_sgv)

        # open client
        cls._cli = ctt.start_cli(CLIENT_CLI_PATH, timeout=DELAY_START_CLI)

    @classmethod
    def tearDownClass(cls):
        ctt.stop_server(cls._srv)

    def test_signal(self):
        # open client
        try:
            child = ctt.start_cli(CLIENT_CLI_PATH, timeout=DELAY_START_CLI)

            # send SIGINT
            child.kill(pexpect.signal.SIGINT)
            ctt.expect(child, pexpect.EOF, timeout=DELAY_START_CLI)

            # open client
            child = ctt.start_cli(CLIENT_CLI_PATH, timeout=DELAY_START_CLI)

            # send SIGTERM
            child.kill(pexpect.signal.SIGTERM)
            ctt.expect(child, pexpect.EOF, timeout=DELAY_START_CLI)
        except BaseException as e:
            self.fail(e)

    def test_01_is_connected(self):
        cmd = "is_connected"
        str_attempt_cli = CLI_EXPECT_CONNECTED
        self._generic_cli_test(cmd, str_attempt_cli)

    def test_02_get_media_list(self):
        cmd = "get_media_list"
        # attempt at minimum the media IPC
        str_attempt_cli = CLI_EXPECT_GET_MEDIA_LIST
        self._generic_cli_test(cmd, str_attempt_cli)

    @unittest2.skipIf(not conf.get_is_show_public_filterchain(),
                      "The filter is maybe not contained in private.")
    def test_03_get_filter_list(self):
        cmd = "get_filter_list"
        # attempt one type of filter
        str_attempt_cli = CLI_EXPECT_GET_FILTER_LIST
        self._generic_cli_test(cmd, str_attempt_cli)

    @unittest2.skipIf(not conf.get_is_show_public_filterchain(),
                      "The filterchain is maybe not contained in private.")
    def test_04_get_filterchain_list(self):
        cmd = "get_filterchain_list"
        # attempt one type of filterchain
        str_attempt_cli = CLI_EXPECT_GET_FILTERCHAIN_LIST
        self._generic_cli_test(cmd, str_attempt_cli)

    def test_05_start_filterchain_execution(self):
        cmd = "start_filterchain_execution"
        args = EXECUTION_NAME_EXAMPLE + " " + CLI_EXPECT_GET_MEDIA_LIST
        # attempt one type of filterchain
        str_attempt_cli = CLI_EXPECT_GET_FILTERCHAIN_LIST
        self._generic_cli_test(cmd, str_attempt_cli, args=args)

    def test_06_get_execution_list(self):
        cmd = "get_execution_list"
        # attempt one type of filterchain
        str_attempt_cli = EXECUTION_NAME_EXAMPLE
        self._generic_cli_test(cmd, str_attempt_cli)

    def test_07_stop_filterchain_execution(self):
        cmd = "stop_filterchain_execution"
        # attempt one type of filterchain
        args = EXECUTION_NAME_EXAMPLE
        str_attempt_cli = EXECUTION_NAME_EXAMPLE
        self._generic_cli_test(cmd, str_attempt_cli, args=args)

    def test_08_exit(self):
        # IMPORTANT, this test need to be executed at the end
        cmd = "exit"
        # exit not exist in the server, attempt a message that precise we
        # cannot close the remote server
        str_attempt_cli = CLI_EXPECT_EXIT
        self._cli.sendline(cmd)
        try:
            ctt.expect(self._cli, str_attempt_cli, timeout=DELAY_START_CLI)
            ctt.expect(self._cli, pexpect.EOF, timeout=DELAY_START_CLI)
        except BaseException as e:
            self.fail(e)

    def _generic_cli_test(self, cmd, str_attempt_cli, args=None):
        str_attempt_srv = SERVER_RECEIVE_CMD % cmd
        not_expect_value = ["WARNING", "ERROR"]
        cmds = cmd if not args else cmd + " " + args
        self._cli.sendline(cmds)
        try:
            ctt.expect(self._cli, str_attempt_cli,
                       not_expect_value=not_expect_value,
                       timeout=DELAY_START_CLI)
            ctt.expect(self._srv, str_attempt_srv,
                       not_expect_value=not_expect_value,
                       timeout=DELAY_START_CLI)
        except BaseException as e:
            self.fail(e)
            # print self._cli.before


class TestCliLocal(unittest2.TestCase):
    """
    Test functionality of all command in cli
    """

    @classmethod
    def setUpClass(cls):
        # 5 minutes, it's enough for all command test
        total_delay_life_sgv = 60 * 5

        # open client
        cls._cli = ctt.start_cli(CLIENT_CLI_LOCAL_PATH,
                                 timeout=total_delay_life_sgv)

    def test_01_is_connected(self):
        cmd = CLI_EXPECT_CONNECTED
        str_attempt_cli = CLI_EXPECT_CONNECTED
        self._generic_cli_test(cmd, str_attempt_cli)

    def test_02_get_media_list(self):
        cmd = "get_media_list"
        # attempt at minimum the media File
        str_attempt_cli = CLI_EXPECT_GET_MEDIA_LIST
        self._generic_cli_test(cmd, str_attempt_cli)

    @unittest2.skipIf(not conf.get_is_show_public_filterchain(),
                      "The filter is maybe not contained in private.")
    def test_03_get_filter_list(self):
        cmd = "get_filter_list"
        # attempt one type of filter
        str_attempt_cli = CLI_EXPECT_GET_FILTER_LIST
        self._generic_cli_test(cmd, str_attempt_cli)

    @unittest2.skipIf(not conf.get_is_show_public_filterchain(),
                      "The filterchain is maybe not contained in private.")
    def test_04_get_filterchain_list(self):
        cmd = "get_filterchain_list"
        # attempt one type of filterchain
        str_attempt_cli = CLI_EXPECT_GET_FILTERCHAIN_LIST
        self._generic_cli_test(cmd, str_attempt_cli)

    def test_05_start_filterchain_execution(self):
        cmd = "start_filterchain_execution"
        args = EXECUTION_NAME_EXAMPLE + " " + CLI_EXPECT_GET_MEDIA_LIST
        # attempt one type of filterchain
        str_attempt_cli = CLI_EXPECT_GET_FILTERCHAIN_LIST
        self._generic_cli_test(cmd, str_attempt_cli, args=args)

    def test_06_get_execution_list(self):
        cmd = "get_execution_list"
        # attempt one type of filterchain
        str_attempt_cli = EXECUTION_NAME_EXAMPLE
        self._generic_cli_test(cmd, str_attempt_cli)

    def test_07_stop_filterchain_execution(self):
        cmd = "stop_filterchain_execution"
        # attempt one type of filterchain
        args = EXECUTION_NAME_EXAMPLE
        str_attempt_cli = EXECUTION_NAME_EXAMPLE
        self._generic_cli_test(cmd, str_attempt_cli, args=args)

    def test_08_exit(self):
        # IMPORTANT, this test need to be executed at the end
        cmd = "exit"
        # exit not exist in the server, attempt a message that precise we
        # cannot close the remote server
        self._cli.sendline(cmd)
        try:
            ctt.expect(self._cli, pexpect.EOF, timeout=DELAY_START_CLI)
        except BaseException as e:
            self.fail(e)

    def _generic_cli_test(self, cmd, str_attempt_cli, args=None):
        not_expect_value = ["WARNING", "ERROR"]
        cmds = cmd if not args else cmd + " " + args
        self._cli.sendline(cmds)
        try:
            ctt.expect(self._cli, str_attempt_cli,
                       not_expect_value=not_expect_value,
                       timeout=DELAY_START_CLI)
        except BaseException as e:
            self.fail(e)


class TestCliSignalLocal(unittest2.TestCase):
    def test_signal(self):
        # open client
        try:
            child = ctt.start_cli(CLIENT_CLI_LOCAL_PATH,
                                  timeout=DELAY_START_CLI)

            # send SIGINT
            child.kill(pexpect.signal.SIGINT)
            ctt.expect(child, pexpect.EOF, timeout=DELAY_START_CLI)

            # open client
            child = ctt.start_cli(CLIENT_CLI_LOCAL_PATH,
                                  timeout=DELAY_START_CLI)

            # send SIGTERM
            child.kill(pexpect.signal.SIGTERM)
            ctt.expect(child, pexpect.EOF, timeout=DELAY_START_CLI)
        except BaseException as e:
            self.fail(e)

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


# TODO test autocomplete in cli
# TODO the cli is suppose to receive real with no other comment
# TODO remove "Nombre de ligne"
# TODO test when close server before closing cli (or sending new command)
def test_cli_cmd():
    """
    Test functionality of all command in cli
    """
    # 15 minutes, it's enough for all command test
    total_delay_life_sgv = 60 * 15
    srv = common_test_tools.start_server(timeout=total_delay_life_sgv)

    # open client
    cli = _open_cli()

    def _test_is_connected_cli():
        cmd = "is_connected"
        str_attempt_cli = "You are connected."
        str_attempt_srv = "Request : %s" % cmd
        cli.sendline(cmd)
        common_test_tools.expect(cli, str_attempt_cli, DELAY_START_CLI)
        common_test_tools.expect(srv, str_attempt_srv, DELAY_START_CLI)
        print("Success %s" % cmd)

    def _test_get_media_list():
        cmd = "get_media_list"
        # attempt at minimum the media File
        str_attempt_cli = "File"
        str_attempt_srv = "Request : %s" % cmd
        cli.sendline(cmd)
        common_test_tools.expect(cli, str_attempt_cli, DELAY_START_CLI)
        common_test_tools.expect(srv, str_attempt_srv, DELAY_START_CLI)
        print("Success %s" % cmd)

    def _test_exit():
        cmd = "exit"
        # exit not exist in the server, attempt a message that precise we
        # cannot close the remote server
        # TODO validate the server has no more print and receive a timeout
        str_attempt_cli = "Cannot close remote server."
        # str_attempt_srv = "Request : %s" % cmd
        cli.sendline(cmd)
        common_test_tools.expect(cli, str_attempt_cli, DELAY_START_CLI)
        # common_test_tools.expect(srv, str_attempt_srv, DELAY_START_CLI)
        print("Success %s" % cmd)

    # test all command
    _test_is_connected_cli()
    _test_get_media_list()
    _test_exit()

    common_test_tools.stop_server(srv)


def _open_cli():
    child = pexpect.spawn(CLIENT_PATH + " cli", timeout=DELAY_START_CLI)
    str_attempt = "(Cmd)"
    common_test_tools.expect(child, str_attempt, DELAY_START_CLI)
    return child

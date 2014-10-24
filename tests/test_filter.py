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

import time
import common_test_tools as ctt
import unittest2
from SeaGoatVision.client.controller.json_client import JsonClient

SERVER_PATH = ctt.SERVER_PATH
DELAY_START_SERVER = ctt.DELAY_START_SERVER
DELAY_CLOSE_SERVER = ctt.DELAY_CLOSE_SERVER
DELAY_START_CLI = ctt.DELAY_START_CLI
SERVER_RECEIVE_CMD = "Request : %s"
SERVER_NOT_EXPECTED = ["ERROR", "WARNING"]

FILTERCHAIN_NAME = "test_filters"
EXECUTION_NAME = "test_filters"
MEDIA_NAME_1 = "generator"
MEDIA_NAME_2 = "Empty"


class TestFilter(unittest2.TestCase):
    """
    Run filter
    """

    @classmethod
    def setUpClass(cls):
        # 5 minutes, it's enough for all command test
        total_delay_life_sgv = 60 * 5
        cls._srv = ctt.start_server(timeout=total_delay_life_sgv, verbose=True)
        cls.ctr = JsonClient(8090, host="localhost")
        if not cls.ctr.is_connected():
            raise BaseException("Cannot connect to server.")

    @classmethod
    def tearDownClass(cls):
        ctt.stop_server(cls._srv)

    def test_01_clean(self):
        self.ctr.delete_filterchain(FILTERCHAIN_NAME)

    def test_02_create_filterchain(self):
        # get all filter
        dct_filters = self.ctr.get_filter_list()
        self.assertTrue(dct_filters)
        # Exception, remove gpu filter
        # TODO all these filter need to be tested, excepted material limitation
        ignore_lst = ["GPUExample", "BGR2Grayscale", "FaceSwap", "resize_img",
                      "BGR2HSVManual", "Watershed", "HoughTransform"]
        filters = [f for f in dct_filters.keys() if
                   not [match for match in ignore_lst if match in f]]
        # print(filters)
        status = self.ctr.modify_filterchain(None, FILTERCHAIN_NAME, filters,
                                             None)
        self.assertTrue(status)

    def test_03_start_execution_generator(self):
        self._start_execution(MEDIA_NAME_1)

    def test_04_stop_execution_generator(self):
        self._stop_execution()

    @unittest2.skip("Waiting for feature #151 for None image in entry.")
    def test_05_start_execution_empty(self):
        self._start_execution(MEDIA_NAME_2)

    @unittest2.skip("Waiting for feature #151 for None image in entry.")
    def test_06_stop_execution_empty(self):
        self._stop_execution()

    def test_07_clean(self):
        self.assertTrue(self.ctr.delete_filterchain(FILTERCHAIN_NAME))

    def _start_execution(self, media_name):
        cmd = SERVER_RECEIVE_CMD % "start_filterchain_execution"
        status = self.ctr.start_filterchain_execution(EXECUTION_NAME,
                                                      media_name,
                                                      FILTERCHAIN_NAME, None,
                                                      None)
        self.assertTrue(status)
        # wait 5 seconds of execution to have enough process
        time.sleep(5)
        ctt.expect(self._srv, cmd, SERVER_NOT_EXPECTED,
                   timeout=DELAY_START_CLI)

    def _stop_execution(self):
        cmd = SERVER_RECEIVE_CMD % "stop_filterchain_execution"
        status = self.ctr.stop_filterchain_execution(EXECUTION_NAME)
        self.assertTrue(status)
        ctt.expect(self._srv, cmd, SERVER_NOT_EXPECTED,
                   timeout=DELAY_START_CLI)

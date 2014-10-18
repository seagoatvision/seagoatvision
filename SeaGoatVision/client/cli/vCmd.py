#! /usr/bin/env python

#    Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Description : Implementation of cmd, command line of python
"""
# SOURCE of this code about the command line :
# http://www.doughellmann.com/PyMOTW/cmd/
import cmd
import socket
from SeaGoatVision.commons import log

logger = log.get_logger(__name__)
DISCONNECTED_MSG = "You are disconnected"


class VCmd(cmd.Cmd):

    def __init__(self, ctr, local=False, host="localhost", port=8090,
                 completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(
            self,
            completekey=completekey,
            stdin=stdin,
            stdout=stdout)
        self.controller = ctr
        self.local = local

    #
    # List of command
    #
    def do_exit(self, line):
        if self.local:
            self.controller.close()
        else:
            print("Cannot close remote server.")
        return True

    def do_is_connected(self, line):
        try:
            status = self.controller.is_connected()
        except socket.error:
            status = False

        if status:
            logger.info("You are connected.")
        else:
            logger.info(DISCONNECTED_MSG)

    def do_get_filter_list(self, line):
        try:
            lst_filter = self.controller.get_filter_list()
        except socket.error:
            logger.error(DISCONNECTED_MSG)
            return

        if lst_filter is not None:
            logger.info(
                "Nombre de ligne %s, tableau : %s" %
                (len(lst_filter), lst_filter))
        else:
            logger.info("No filterlist")

    def do_get_filterchain_list(self, line):
        try:
            lst_filter_chain = self.controller.get_filterchain_list()
        except socket.error:
            logger.error(DISCONNECTED_MSG)
            return

        lst_name = [item.get("name") for item in lst_filter_chain]
        if lst_filter_chain is not None:
            logger.info(
                "Nombre de ligne %s, tableau : %s" %
                (len(lst_filter_chain), lst_name))
        else:
            logger.info("No lst_filter_chain")
        # logger.info(lst_name)

    def do_add_output_observer(self, line):
        # execution_name
        param = line.split()
        try:
            self.controller.add_output_observer(param[0])
        except socket.error:
            logger.error(DISCONNECTED_MSG)

    def do_stop_output_observer(self, line):
        # execution_name
        param = line.split()
        try:
            self.controller.remove_output_observer(param[0])
        except socket.error:
            logger.error(DISCONNECTED_MSG)

    def do_start_filterchain_execution(self, line):
        # execution_name, media_name, filterchain_name
        param = line.split()
        name = ""
        if len(param):
            name = param[0]
        media = ""
        if len(param) > 1:
            media = param[1]
            if media == "None":
                media = ""
        filterchain = ""
        if len(param) > 2:
            filterchain = param[2]
            if filterchain == "None":
                filterchain = ""

        try:
            self.controller.start_filterchain_execution(
                name, media, filterchain, None, False)
        except socket.error:
            logger.error(DISCONNECTED_MSG)

    def do_stop_filterchain_execution(self, line):
        # execution_name
        param = line.split()
        try:
            self.controller.stop_filterchain_execution(param[0])
        except socket.error:
            logger.error(DISCONNECTED_MSG)

    def do_start_record(self, line):
        # media_name
        param = line.split()
        path = None
        if len(param) > 1:
            path = param[1]

        try:
            self.controller.start_record(param[0], path)
        except socket.error:
            logger.error(DISCONNECTED_MSG)

    def do_stop_record(self, line):
        # media_name
        param = line.split()
        try:
            self.controller.stop_record(param[0])
        except socket.error:
            logger.error(DISCONNECTED_MSG)

    def do_get_media_list(self, line):
        try:
            lst_media = self.controller.get_media_list()
        except socket.error:
            logger.error(DISCONNECTED_MSG)
            return

        if lst_media is not None:
            logger.info("Media list : %s" % lst_media)
        else:
            logger.info("No media")
        # logger.info(lst_media)

    def do_EOF(self, line):
        # Redo last command
        return True

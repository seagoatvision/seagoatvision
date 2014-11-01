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

        self._media_list = self.controller.get_media_list()
        self._filterchain_list = self.controller.get_filterchain_list()

    #
    # List of command
    #
    def do_exit(self, line):
        if not self.local:
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

        logger.info(lst_filter)

    def do_get_filterchain_list(self, line):
        try:
            lst_filter_chain = self.controller.get_filterchain_list()
        except socket.error:
            logger.error(DISCONNECTED_MSG)
            return

        logger.info([item.get("name") for item in lst_filter_chain])

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
            if name == "None":
                name = None
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

    def help_start_filterchain_execution(self):
        info = ['start_filterchain_execution [name] [media] [filterchain]',
                'For default value, use None.',
                'Media and Filterchain can be auto-complete.']
        print('\n'.join(info))

    def complete_start_filterchain_execution(self, text, line, begidx, endidx):
        param = line.split()
        completions = None
        if len(param) == 2 or (len(param) == 3 and line[-1] != ' '):
            # auto-complete media
            lst_media = self._media_list.keys()
            if not text:
                completions = lst_media[:]
            else:
                completions = [f for f in lst_media if
                               f.startswith(text)]
        elif len(param) == 3 or (len(param) == 4 and line[-1] != ' '):
            # auto-complete filterchain
            lst_filterchain = [f.get("name") for f in self._filterchain_list]
            if not text:
                completions = lst_filterchain
            else:
                completions = [f for f in lst_filterchain if
                               f.startswith(text)]
        return completions

    def do_stop_filterchain_execution(self, line):
        # execution_name
        param = line.split()
        if not param:
            logger.error("Missing param Execution_name.")
            return
        try:
            self.controller.stop_filterchain_execution(param[0])
        except socket.error:
            logger.error(DISCONNECTED_MSG)

    def help_stop_filterchain_execution(self):
        info = ['stop_filterchain_execution name',
                'Name can be auto-complete.']
        print('\n'.join(info))

    def complete_stop_filterchain_execution(self, text, line, begidx, endidx):
        param = line.split()
        completions = None
        if len(param) == 1 or (len(param) == 2 and line[-1] != ' '):
            # auto-complete media
            lst_execution = self.controller.get_execution_list()
            if not text:
                completions = lst_execution[:]
            else:
                completions = [f for f in lst_execution if
                               f.startswith(text)]
        return completions

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

        logger.info(lst_media)

    def do_get_execution_list(self, line):
        try:
            lst_execution = self.controller.get_execution_list()
        except socket.error:
            logger.error(DISCONNECTED_MSG)
            return

        logger.info(lst_execution)

    def do_EOF(self, line):
        # Redo last command
        return True

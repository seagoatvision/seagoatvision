#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
# This file is part of SeaGoatVision.
#
# SeaGoatVision is free software: you can redistribute it and/or modify
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

from SeaGoatVision.server.media.media_streaming import MediaStreaming
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.commons.param import Param
from SeaGoatVision.commons import log
import goprocontroller

logger = log.get_logger(__name__)


class GoPro(MediaStreaming):
    """Return images from the GoPro."""

    def __init__(self, config):
        # Go into configuration/template_media for more information
        self.config = Configuration()
        self.own_config = config
        super(GoPro, self).__init__()
        self.media_name = config.name
        self.camera = None
        self._is_opened = True

        self._lst_mode = ['still', 'video']
        self._create_params()

    def open(self):
        self.camera = goprocontroller.GoPro(ip=self.own_config.ip,
                                            password=self.own_config.password)
        if self.camera:
            # call open when video is ready
            return MediaStreaming.open(self)
        return False

    def next(self):
        try:
            success, base_img = self.camera.getImageNP()
            return base_img
        except Exception as e:
            print(e)

    def close(self):
        MediaStreaming.close(self)

    def _create_params(self):
        group = "Operation"

        self.param_power = Param("power", True)
        self.param_power.add_notify(self._update_cam_state)
        self.param_power.set_description("Power on/off.")
        self.param_power.add_group(group)

        self.param_record = Param("record", False)
        self.param_record.add_notify(self._update_cam_state)
        self.param_record.set_description("Active record.")
        self.param_record.add_group(group)

        group = "Mode"

        lst_mode = self._lst_mode
        self.param_mode = Param("mode", lst_mode[0], lst_value=lst_mode)
        self.param_mode.add_notify(self._update_cam_mode)
        self.param_mode.set_description("Change mode of record.")
        self.param_mode.add_group(group)

    def _update_cam_state(self, param):
        # cmd power_on, power_off, record_on, record_off
        name = self.get_name()
        if not self.camera:
            logger.warning("Camera %s is not active." % name)
            return
        value = bool(param.get())
        cmd = '%s_%s' % (name, 'on' if value else 'off')
        self.camera.sendCommand(cmd)

    def _update_cam_mode(self, param):
        # cmd power_on, power_off, record_on, record_off
        name = self.get_name()
        if not self.camera:
            logger.warning("Camera %s is not active." % name)
            return
        value = param.get()
        if value not in self._lst_mode:
            logger.warning("Camera %s unrecognize mode %s." % (name, value))
            return
        cmd = 'mode_%s' % value
        self.camera.sendCommand(cmd)

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

from SeaGoatVision.server.media.implementation.pygame_cam import PygameCam


class ConfPygameCam:
    def __init__(self):
        self.media = PygameCam
        self.name = "pygame_cam"
        self.no = "0"
        self.path = "/dev/video%s" % self.no
        self.default_fps = None

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

from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.filter import Filter
import PIL
from PIL import ImageDraw
import numpy as np


class DrawArc(Filter):
    """Draw an arc in the image"""

    def __init__(self):
        Filter.__init__(self)
        self._x_max = 800
        self._y_max = 600
        self._create_param()

    def _create_param(self):
        group_color = "Color"
        group_position = "Position"
        group_size = "Size"
        group_angle = "Angle"

        self.x = Param('x', 0, max_v=self._x_max, min_v=0)
        self.x.add_group(group_position)
        self.y = Param('y', 0, max_v=self._y_max, min_v=0)
        self.y.add_group(group_position)

        self.width = Param('width', 100, max_v=1000, min_v=0)
        self.width.add_group(group_size)
        self.height = Param('height', 100, max_v=1000, min_v=0, is_lock=True)
        self.height.add_group(group_size)
        self.is_symmetric = Param('is_symmetric', True)
        self.is_symmetric.add_notify(self._change_symmetry)
        self.is_symmetric.add_group(group_size)

        self.position_angle = Param('position_angle', 0, min_v=0, max_v=360)
        self.position_angle.add_group(group_angle)
        self.size_angle = Param('size_angle', 45, min_v=0, max_v=360)
        self.size_angle.add_group(group_angle)

        self.color_r = Param('red', 255, min_v=0, max_v=255)
        self.color_r.add_group(group_color)
        self.color_g = Param('green', 0, min_v=0, max_v=255)
        self.color_g.add_group(group_color)
        self.color_b = Param('blue', 0, min_v=0, max_v=255)
        self.color_b.add_group(group_color)
        self.color_alpha = Param('alpha', 0, min_v=0, max_v=100)
        self.color_alpha.add_group(group_color)

    def execute(self, image):
        """
        Draw an arc.
        :param image: input
        :return: output
        """
        img_pil = PIL.Image.fromarray(image)
        draw = ImageDraw.Draw(img_pil)

        color = (self.color_b.get(), self.color_g.get(), self.color_r.get(),
                 self.color_alpha.get())

        width = self.width.get()
        height = width if self.is_symmetric.get() else self.height.get()
        x = self.x.get()
        y = self.y.get()
        box = (x, y, width + x, height + y)
        position_angle = self.position_angle.get()
        size_angle = self.size_angle.get() + position_angle

        draw.arc(box, position_angle, size_angle, fill=color)

        return np.array(img_pil)

    def _change_symmetry(self, param):
        self.height.set_lock(param.get())

/*
 * Copyright (C) 2014 Octets - octets.etsmtl.ca
 *
 * This file is part of SeaGoatVision.
 *
 * SeaGoatVision is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include "opencv2/opencv.hpp"

#define DOCSTRING "Resize the image"

const char* WIDTH = "width";
const char* HEIGHT = "height";

void init()
{
    param_int(WIDTH, 100, 1, 4096);
    param_int(HEIGHT, 100, 1, 4096);
}

cv::Mat execute(cv::Mat image)
{
    int width = param_get_int(WIDTH);
    int weight = param_get_int(HEIGHT);
    cv::Size size(width, weight);
    cv::Mat dst;
    cv::resize(image, dst, size);
    return dst;
}

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Generic Drivetrain model.

Models a drivetrain on an frc robot.

"""

import logging
import pandas as pd
import numpy as np

from frc_rekt.motor import Motor
from frc_rekt.wheel import Wheel

# Pandas options
pd.set_option('max_rows', 121)
pd.set_option('max_columns', 132)
pd.set_option('expand_frame_repr', False)

# just a convenience, so we dont have to type np.poly.poly
POLY = np.polynomial.polynomial


class Drivetrain(object):
    """Model of a Drivetrain."""

    def __init__(self, wheel=None, motor=None, length=34, width=28):
        """Drivetrain.

        :param wheel: what wheel is used on the wheelbase
        :type wheel: `frc_rekt.wheel.Wheel`
        :param motor: What motor the wheelbase uses
        :type motor: `frc_rekt.motor.Motor`
        :param length: the length of the wheelbase, from wheel center to wheel center in inches
        :type length: int float
        :param width: the width of the wheelbase, from wheel center to wheel center in inches
        :type width: int float

        """
        self._logger = logging.getLogger(__name__)
        # store diameter in meters
        self._length = float(length) * 0.0254
        self._width = float(width) * 0.0254
        if not wheel:
            wheel = Wheel()
        self.wheel = wheel
        if not motor:
            motor = Motor()
        self.motor = motor
        self._logger.debug('%s created', str(self))

    def __str__(self):
        """Represent a Drivetrain."""
        return 'Drivetrain({wheel}, {motor}, {length}, {width})'.format(
            wheel=str(self.wheel),
            motor=str(self.motor),
            length=self.length,
            width=self.width)

    @property
    def length(self):
        """Wheelbase length in inches."""
        return self._length / 0.0254

    @property
    def width(self):
        """Wheelbase width in inches."""
        return self._width / 0.0254

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Wheel model.

Models a wheel on an frc robot.

"""

import logging
import pandas as pd
import numpy as np

# Pandas options
pd.set_option('max_rows', 121)
pd.set_option('max_columns', 132)
pd.set_option('expand_frame_repr', False)

# just a convenience, so we dont have to type np.poly.poly
POLY = np.polynomial.polynomial


class Wheel(object):  # pylint: disable=too-few-public-methods
    """Model of a Mainbreaker."""

    def __init__(self, diameter=4.0, cof=1.3, torque=0.0):
        """Wheel.

        :param diameter: The diameter of the wheel in inches
        :type diameter: int float
        :param cof: The coefficient of friction of the wheel
        :type cof: int float

        """
        self._logger = logging.getLogger(__name__)
        # store diameter in meters
        self._diameter = float(diameter) * 0.0254
        self.cof = float(cof)
        self.torque = float(torque)
        self._logger.debug('%s created', str(self))

    def __repr__(self):
        """Represent a wheel."""
        return 'Wheel(diameter={0}, cof={1}, torque={2})'.format(
            self.diameter, self.cof, self.torque)

    @property
    def diameter(self):
        """Wheel diameter in inches."""
        return self._diameter / 0.0254

    @property
    def _force(self):
        """Force at wheel in N*m."""
        return self.torque / (self._diameter / 2.0)

    @property
    def force(self):
        """Force at wheel in ft*lbs."""
        return self._force * 0.737562149277

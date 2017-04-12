#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Gearbox model.

Models a gearbox on an frc robot.

"""

import logging
import pandas as pd
import numpy as np

from frc_rekt.motor import Motor

# Pandas options
pd.set_option('max_rows', 121)
pd.set_option('max_columns', 132)
pd.set_option('expand_frame_repr', False)

# just a convenience, so we dont have to type np.poly.poly
POLY = np.polynomial.polynomial


class Gearbox(object):  # pylint: disable=too-few-public-methods
    """Model of a Gearbox."""

    def __init__(self, motors=None, gears=None, efficiency=0.8):
        """Gearbox.

        :param motors: The motors attached to the gearbox
        :type motors: list
        :param gears: The gears in the gearbox
        :type gears: list
        :param efficiency: The efficiency of the gearbox
        :type efficiency: float

        """
        self._logger = logging.getLogger(__name__)
        # store diameter in meters
        self._gears = gears
        if not self._gears:
            self._gears = [(14, 50), (16, 48)]
        self._motors = motors
        if not self._motors:
            self._motors = [Motor(), Motor(), Motor()]
        self._efficiency = efficiency
        self._logger.debug('%s created', str(self))

    @property
    def mechanical_advantage(self):
        """Gearbox mechanical advantage."""
        mechanical_advantage = 1.0
        for gear_pair in self._gears:
            mechanical_advantage = mechanical_advantage * (
                float(gear_pair[1]) / float(gear_pair[0]))
        return mechanical_advantage

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Battery model.

Models a battery on an frc robot.

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


class Battery(object):  # pylint: disable=too-few-public-methods
    """Model of a Battery."""

    def __init__(self,
                 starting_voltage=13.2,
                 load=0,
                 internal_resistance=0.012):
        """Battery.

        :param starting_voltage: The starting voltage of the battery
        :type starting_voltage: int float
        :param load: The current battery load
        :type load: float
        :param internal_resistance: The internal resistance of the battery in ohms
        :type internal_resistance: float

        """
        self._logger = logging.getLogger(__name__)
        self._voltage = float(starting_voltage)
        self.load = float(load)
        self.internal_resistance = internal_resistance
        self._logger.debug('%s created', str(self))

    def voltage(self):
        """Voltage of battery."""
        # V = I*R
        # internal resistance is "in series" w_ith the voltage source
        return self._voltage - (self.load * self.internal_resistance)

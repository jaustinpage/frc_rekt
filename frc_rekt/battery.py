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

    def __init__(self, starting_voltage=13.2):
        """Battery.

        :param starting_voltage: The starting voltage of the battery
        :type starting_voltage: int float

        """
        self._logger = logging.getLogger(__name__)
        self.starting_voltage = float(starting_voltage)
        self._logger.debug('%s created', str(self))

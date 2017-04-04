#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""MainBreaker model.

Models a main breaker on an frc robot. Uses data from datasheet

"""

import logging
import pandas as pd
import numpy as np

from frc_rekt.helpers import get_file_encoding

# Pandas options
pd.set_option('max_rows', 121)
pd.set_option('max_columns', 132)
pd.set_option('expand_frame_repr', False)

# just a convenience, so we dont have to type np.poly.poly
POLY = np.polynomial.polynomial


class MainBreaker(object):  # pylint: disable=too-few-public-methods
    """Model of a Mainbreaker."""

    def __init__(self, ambient_temp=25):
        """MainBreaker.

        :param ambient_temp: The ambient temperature of the breaker
        :type ambient_temp: int float

        """
        self.logger = logging.getLogger(__name__)
        self.ambient_temp = ambient_temp
        self._temp_derate_min_frames = self._get_temp_derate_frames()
        self._trip_time_frames = self._get_trip_time_frames()
        self.logger.debug('Main Breaker created at %s degrees C',
                          self.ambient_temp)

    @staticmethod
    def _get_file_name(datatype='temp_derate', boundary='min'):
        directory = 'data/data_sheets'
        filename = '120-main-breaker-{0}-{1}.csv'.format(datatype, boundary)
        path = '{0}/{1}'.format(directory, filename)
        encoding = get_file_encoding(path)
        return path, encoding

    def _get_frame(self, datatype='temp_derate', boundary='min'):
        file_path, encoding = self._get_file_name(
            datatype=datatype, boundary=boundary)

        self.logger.debug('Opening dataframe: %s', file_path)
        d_frame = pd.read_csv(file_path, encoding=encoding)

        self.logger.debug('Opened dataframe: %s', d_frame)
        # Rename columns
        self.logger.debug('Main Breaker %s-%s', datatype, boundary)
        return d_frame

    def _get_temp_derate_frames(self):
        frames = {
            'min': self._get_frame(datatype='temp_derate', boundary='min'),
            'max': self._get_frame(datatype='temp_derate', boundary='max')
        }
        return frames

    def _get_trip_time_frames(self):
        frames = {
            'min': self._get_frame(datatype='trip_time', boundary='min'),
            'max': self._get_frame(datatype='trip_time', boundary='max')
        }
        return frames

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""MainBreaker model.

Models a main breaker on an frc robot. Uses data from datasheet

"""

import logging
import pandas as pd
import numpy as np

from scipy import optimize

from frc_rekt.helpers import get_file_encoding, plot_func

# Pandas options
pd.set_option('max_rows', 121)
pd.set_option('max_columns', 132)
pd.set_option('expand_frame_repr', False)

# just a convenience, so we dont have to type np.poly.poly
POLY = np.polynomial.polynomial


class MainBreaker(object):  # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """Model of a Mainbreaker."""

    def __init__(self, ambient_temp=25):
        """MainBreaker.

        :param ambient_temp: The ambient temperature of the breaker
        :type ambient_temp: int float

        """
        self._logger = logging.getLogger(__name__)
        self.ambient_temp = ambient_temp
        self._temp_derate_min_frames = self._get_temp_derate_frames()
        self._trip_time_frames = self._get_trip_time_frames()
        self._generate_functions()
        self._logger.debug('Main Breaker created at %s degrees C',
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

        self._logger.debug('Opening dataframe: %s', file_path)
        d_frame = pd.DataFrame(
            pd.read_csv(file_path, encoding=encoding, comment='#')
        )  # The cast to DataFrame is due to bug: https://github.com/PyCQA/pylint/issues/1161

        self._logger.debug('Opened dataframe: %s', d_frame)
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

    @staticmethod
    def _fit_func_factory(a=None, b=None, c=None, d=None, e=None):
        # Specific with correction
        if a and b and c and d and e:

            def func(x):
                """Specific Function."""
                return a * ((b * (x + c))**d) + e

        # Specific without correction
        elif a and b and c and d:

            def func(x):
                """Specific Function."""
                return a * ((b * (x + c))**d)

        # Generic, which we have scipy.optimize.curve_fit run on
        # scipy.optimize.curve_fit will then give us a, b, c, d,
        # however, scipy.optimize has touble with e. We correct e "by hand"
        # at the end.
        else:

            def func(x, a, b, c, d):  # pylint: disable=too-many-arguments
                """Generic Function."""
                return a * ((b * (x + c))**d)

        return func

    def _generate_functions(self, plot=False):
        self.trip_time_min = self._generate_func(
            datatype='trip_time',
            boundary='min',
            plot=plot,
            fit_func_factory=self._fit_func_factory)
        self.trip_time_max = self._generate_func(
            datatype='trip_time',
            boundary='max',
            plot=plot,
            fit_func_factory=self._fit_func_factory)
        self.temp_derate_min = self._generate_func(
            datatype='temp_derate', boundary='min', plot=plot)
        self.temp_derate_max = self._generate_func(
            datatype='temp_derate', boundary='max', plot=plot)

    @staticmethod
    def _generate_poly_fit(x, y, deg=3):
        coefs = POLY.polyfit(x, y, deg)
        func = POLY.Polynomial(coefs)
        return func

    @staticmethod
    def _generate_func_fit(func_factory, x, y):
        popt, pcov = optimize.curve_fit(func_factory(), x, y)
        logging.debug(popt)
        logging.debug(pcov)
        # Static shift to have the end condition be nice
        unshifted_func = func_factory(*popt)
        end_diff = y.iloc[-1] - unshifted_func(x.iloc[-1])
        logging.debug("end diff: %s", end_diff)
        popt_shifted = np.append(popt, end_diff)
        return func_factory(*popt_shifted)

    def _generate_func(self,
                       datatype='trip_time',
                       boundary='min',
                       plot=False,
                       fit_func_factory=None):
        d_frame = self._get_frame(datatype=datatype, boundary=boundary)
        logging.debug("d_frame to fit: %s", d_frame)
        x = d_frame[str(d_frame.columns[0])]
        y = d_frame[str(d_frame.columns[1])]
        if not fit_func_factory:
            fitted_func = self._generate_poly_fit(x, y)
        else:
            fitted_func = self._generate_func_fit(fit_func_factory, x, y)

        if plot:
            plot_func(d_frame, fitted_func, title='main_breaker')
        return fitted_func

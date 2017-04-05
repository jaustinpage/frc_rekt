#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Model of an frc Motor.

Models an frc motor. Uses data from motors.vex.com.

"""

import logging
import pandas as pd
import numpy as np

from frc_rekt.helpers import get_file_encoding, plot_func

# Pandas options
pd.set_option('max_rows', 121)
pd.set_option('max_columns', 132)
pd.set_option('expand_frame_repr', False)

# just a convenience, so we dont have to type np.poly.poly
POLY = np.polynomial.polynomial


class Motor(object):  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Models a motor."""

    motor_types = ['cim', 'mini-cim', '775pro', 'bag']
    _stall_voltages = [2, 4, 6, 8, 10, 12]
    _motor_curve_voltage = 12.0

    def __init__(self, motor_type='cim', speed=0.0, voltage=0.0):
        """Motor.

        :param motor_type: The type of motor to model
        :type motor_type: str
        :param speed: The speed the motor is turning at
        :type speed: float
        :param voltage: The voltage being supplied to the motor
        :type voltage: float

        """
        self._logger = logging.getLogger(__name__)
        self.motor_type = motor_type
        self.speed = speed
        self.voltage = voltage
        self.curve_frame = self._get_curve_frame()
        self.stall_frames = self._get_stall_frames()
        self._generate_functions()
        self._logger.debug('%s Motor created', self.motor_type)

    def _get_file_name(self, voltage=None):
        data_folder = 'data/vex'
        curve_data_date = {
            'cim': '20151104',
            'mini-cim': '20151207',
            '775pro': '20151208',
            'bag': '20151207'
        }
        stall_data_date = {
            'cim': '20151104',
            'mini-cim': '20151209',
            '775pro': '20151209',
            'bag': '20151207'
        }
        date = curve_data_date[self.motor_type]
        data_type = 'motor-curve-data'
        if voltage:
            data_type = 'locked-rotor-data-{voltage}v'.format(voltage=voltage)
            date = stall_data_date[self.motor_type]

        file_name = '{motor_type}-{data_type}-{date}.csv'.format(
            motor_type=self.motor_type, data_type=data_type, date=date)
        file_path = '{data_folder}/{motor_type}/{file_name}'.format(
            data_folder=data_folder,
            motor_type=self.motor_type,
            file_name=file_name)
        encoding = get_file_encoding(file_path)
        logging.debug('file_path: %s, encoding: %s', file_path, encoding)
        return file_path, encoding

    def _get_curve_frame(self):
        file_path, encoding = self._get_file_name()

        self._logger.debug('Opening curve: %s', file_path)
        curve_frame = pd.DataFrame(
            pd.read_csv(file_path, encoding=encoding)
        )  # The cast to DataFrame is due to bug: https://github.com/PyCQA/pylint/issues/1161
        self._logger.debug('Opened Curve: %s', curve_frame)

        # Rename columns
        curve_frame.rename(
            columns={
                'Speed (RPM)': 'speed',
                'Torque (N·m)': 'torque',
                'Current (A)': 'current',
                'Supplied Power (W)': 'supplied_power',
                'Output Power (W)': 'output_power',
                'Efficiency (%)': 'efficiency',
                'Power Dissipation (W)': 'power_dissipation'
            },
            inplace=True)
        # Convert to si units
        curve_frame['speed'] = curve_frame[
            'speed'] / 60.0  # revolutions / second
        curve_frame['efficiency'] = curve_frame[
            'efficiency'] / 100.0  # percentage scaled to 1
        self._logger.debug('Motor Curve: %s', curve_frame)
        return curve_frame

    def _get_stall_frames(self):
        stall_frames = {}
        for voltage in self._stall_voltages:
            file_path, encoding = self._get_file_name(voltage=voltage)

            stall_frame = pd.DataFrame(
                pd.read_csv(file_path, encoding=encoding)
            )  # The cast to DataFrame is due to bug: https://github.com/PyCQA/pylint/issues/1161
            # rename columns
            stall_frame.rename(
                columns={
                    'Time': 'time',
                    'Time (s)': 'time',
                    'Amps': 'current',
                    'Current (A)': 'current',
                    'Volts': 'voltage',
                    'Voltage (V)': 'voltage',
                    'Torque 2V (N · m)': 'torque',
                    'Torque 4V (N · m)': 'torque',
                    'Torque 6V (N · m)': 'torque',
                    'Torque 8V (N · m)': 'torque',
                    'Torque 10V (N · m)': 'torque',
                    'Torque 12V (N · m)': 'torque'
                },
                inplace=True)
            stall_frames[voltage] = stall_frame
        self._logger.debug('Stall frames: %s', stall_frames)
        return stall_frames

    def _generate_functions(self):
        self.current_func = self._generate_basic_function('current')
        self.torque_func = self._generate_basic_function('torque')
        self.voltage_scaled_current = self._gen_voltage_scaled_func('current')
        self.voltage_scaled_torque = self._gen_voltage_scaled_func('torque')

    def _generate_basic_function(self, y_label, plot=False):
        x = self.curve_frame['speed'].values
        y = self.curve_frame[y_label].values

        coefs = POLY.polyfit(x=x, y=y, deg=1)
        current_func = POLY.Polynomial(coefs)
        if plot:
            plot_func(self.curve_frame, current_func, 'speed', y_label,
                      self.motor_type)
        return current_func

    def _choose_stall_indexes(self):
        time = [0]
        current = [0]
        voltage = [0]
        torque = [0]
        test_voltage = [0]

        # Get the first 10 values, picked 10 after looking at
        # 775pro 12v locked rotor test data
        # Then, we get the max power in those first 10 data points
        for test_v in self._stall_voltages:
            head = self.stall_frames[test_v].iloc[1:10]
            max_power_index = 0
            max_power = 0
            for index, row in head.iterrows():
                power = row['current'] * row['voltage']
                if power > max_power:
                    max_power_index = index
                    max_power = power
            test_voltage.append(test_v)
            time.append(
                self.stall_frames[test_v].iloc[max_power_index]['time'])
            current.append(
                self.stall_frames[test_v].iloc[max_power_index]['current'])
            voltage.append(
                self.stall_frames[test_v].iloc[max_power_index]['voltage'])
            torque.append(
                self.stall_frames[test_v].iloc[max_power_index]['torque'])

        stall_index = {
            'test_voltage': test_voltage,
            'time': time,
            'current': current,
            'voltage': voltage,
            'torque': torque
        }
        return pd.DataFrame(stall_index)

    def _gen_voltage_scaled_func(self, y_label, plot=False):
        percent_label = '{0}_percent'.format(y_label)

        stall_df = self._choose_stall_indexes()
        y_label_12v = stall_df[y_label].iloc[6]
        stall_df[percent_label] = stall_df[y_label] / y_label_12v
        x = stall_df['voltage']
        y = stall_df[percent_label]
        coefs = POLY.polyfit(
            x=x, y=y,
            deg=[1, 2,
                 3])  # Don't use the 0th term because we want to intercept 0,0
        vs_func = POLY.Polynomial(coefs)
        if plot:
            predict_df = [{'voltage': 13}, {'voltage': 14}]
            stall_df = stall_df.append(predict_df, ignore_index=True)  # pylint: disable=redefined-variable-type
            plot_func(stall_df, vs_func, 'voltage', percent_label,
                      self.motor_type)
        return vs_func

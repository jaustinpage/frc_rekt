#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import collections
import logging
import pandas as pd
import pint
import pprint
import numpy as np
import magic
import math
import matplotlib.pyplot as plt

# Pandas options
pd.set_option('max_rows', 121)
pd.set_option('max_columns', 132)
pd.set_option('expand_frame_repr', False)

# just a convenience, so we dont have to type np.poly.poly
poly = np.polynomial.polynomial


class Motor(object):
    def __init__(self, motor_type='cim', speed=0.0, voltage=0.0):
        self.logger = logging.getLogger(__name__)
        self.motor_type = motor_type
        self.speed = speed
        self.voltage = voltage
        self.motor_curve_voltage = 12.0
        self.stall_voltages = [2, 4, 6, 8, 10, 12]
        self.curve_frame = self.get_curve_frame()
        self.stall_frames = self.get_stall_frames()
        self.generate_functions()
        self.logger.debug(
            '{motor_type} Motor created'.format(motor_type=self.motor_type))

    def get_file_encoding(self, file_path):
        m = magic.Magic(mime_encoding=True)
        encoding = m.from_file(file_path)
        return encoding

    def get_file_name(self, voltage=None):
        '''
        returns the motor curve if no voltage is supplied, else
        returns locked rotor test data for that voltage
        '''
        data_folder = 'vex_data'
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
        encoding = self.get_file_encoding(file_path)
        logging.debug(
            'file_path: {0}, encoding: {1}'.format(file_path, encoding))
        return file_path, encoding

    def get_curve_frame(self):
        file_path, encoding = self.get_file_name()
        try:
            self.logger.debug(
                'Opening curve: {file_path}'.format(file_path=file_path))
            curve_frame = pd.read_csv(file_path, encoding=encoding)
        except KeyError as e:
            raise e
        self.logger.debug('Opened Curve: {0}'.format(curve_frame))
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
        self.logger.debug('Motor Curve: {0}'.format(curve_frame))
        return curve_frame

    def get_stall_frames(self):
        stall_frames = {}
        for voltage in self.stall_voltages:
            file_path, encoding = self.get_file_name(voltage=voltage)
            try:
                stall_frame = pd.read_csv(file_path, encoding=encoding)
            except KeyError as e:
                raise e
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
        self.logger.debug('Stall frames: {0}'.format(stall_frames))
        return stall_frames

    def generate_functions(self):
        self.current_func = self.generate_basic_function('current')
        self.torque_func = self.generate_basic_function('torque')

    def plot_fit(self, dataframe, fit_func, x_label, y_label):
        dataframe['fit'] = fit_func(dataframe[x_label])
        plot_df = dataframe.loc[:, [x_label, y_label, 'fit']]
        plot_df.plot(x=x_label)

    def generate_basic_function(self, y_label, plot=False):
        x = self.curve_frame['speed'].values
        y = self.curve_frame[y_label].values

        coefs = poly.polyfit(x=x, y=y, deg=1)
        current_func = poly.Polynomial(coefs)
        if plot:
            self.plot_fit(self.curve_frame, current_func, 'speed', y_label)
        return current_func

    def choose_stall_indexes(self, time_index=None):
        time = [0]
        current = [0]
        voltage = [0]
        torque = [0]
        test_voltage = [0]

        # Get the first 10 values, picked 10 after looking at 
        # 775pro 12v locked rotor test data
        # Then, we get the max power in those first 10 data points
        for test_v in self.stall_voltages:
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

    def generate_voltage_scaled_function(self, y_label, plot=False):
        percent_label = '{0}_percent'.format(y_label)

        stall_df = self.choose_stall_indexes()
        y_label_12v = stall_df[y_label].iloc[6]
        stall_df[percent_label] = stall_df[y_label] / y_label_12v
        x = stall_df['voltage']
        y = stall_df[percent_label]
        coefs = poly.polyfit(
            x=x, y=y,
            deg=[1, 2,
                 3])  # Don't use the 0th term because we want to intercept 0,0
        vs_func = poly.Polynomial(coefs)
        if plot:
            predict_df = [{'voltage': 13}, {'voltage': 14}]
            stall_df = stall_df.append(predict_df, ignore_index=True)
            self.plot_fit(stall_df, vs_func, 'voltage', percent_label)
        return vs_func


def main():
    logging.basicConfig(level=logging.INFO)
    cim_motor = Motor(motor_type='cim')
    cim_motor.generate_voltage_scaled_function('current', plot=True)
    cim_motor.generate_voltage_scaled_function('torque', plot=True)
    minicim_motor = Motor(motor_type='mini-cim')
    minicim_motor.generate_voltage_scaled_function('current', plot=True)
    minicim_motor.generate_voltage_scaled_function('torque', plot=True)
    bag_motor = Motor(motor_type='bag')
    bag_motor.generate_voltage_scaled_function('current', plot=True)
    bag_motor.generate_voltage_scaled_function('torque', plot=True)
    pro_motor = Motor(motor_type='775pro')
    pro_motor.generate_voltage_scaled_function('current', plot=True)
    pro_motor.generate_voltage_scaled_function('torque', plot=True)
    plt.show()


if __name__ == '__main__':
    main()

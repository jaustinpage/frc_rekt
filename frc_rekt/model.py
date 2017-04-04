#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# pylint: skip-file

import collections
import pandas as pd
import pint
import pprint
import numpy as np
import math
import matplotlib.pyplot as plt

# Pandas options
pd.set_option('max_rows', 121)
pd.set_option('max_columns', 132)
pd.set_option('expand_frame_repr', False)

# just a convenience, so we dont have to type np.poly.poly
poly = np.polynomial.polynomial


class Battery(object):
    def __init__(self, nominal_voltage=12.8):
        pass

    def generate_equations(self):
        pass


# Robot constants
# TODO: Refactor with new motor class
class TankRobot(object):
    def __init__(self,
                 mass=154,
                 gear_ratio=8.0,
                 wheel_diameter=4.0,
                 wheel_friction=1.35,
                 motor_type='cim',
                 motors_per_side=3,
                 gearbox_efficiency=0.8,
                 reserve_acceleration=0.2,
                 battery_min_allowed_voltage=8.0,
                 battery_nominal_voltage=12.8,
                 battery_internal_resistance=0.008):
        # Initialize and set to si units
        self.mass = mass * 0.453592
        self.gear_ratio = gear_ratio
        self.wheel_diameter = wheel_diameter * 0.0254
        self.wheel_perimeter = self.wheel_diameter * math.pi
        self.wheel_friction = wheel_friction
        self.motor_type = motor_type
        self.motors_per_side = motors_per_side
        self.motors = self.motors_per_side * 2
        self.gearbox_efficiency = gearbox_efficiency
        self.reserve_acceleration = reserve_acceleration
        self.battery_min_allowed_voltage = battery_min_allowed_voltage
        self.battery_nominal_voltage = battery_nominal_voltage
        self.battery_internal_resistance = battery_internal_resistance
        self.curve_voltage = 12.0  # voltage that was used when generating the motor curve

        self.motor_curve = self.generate_motor_curve()
        self.voltage_limited_accel = self.find_voltage_limited_acceleration_equation(
        )
        self.max_pwm_allowed_equation = self.find_max_pwm_allowed_equation()

    def __str__(self):
        robot_parameters = {
            'mass': self.mass,
            'gear_ratio': self.gear_ratio,
            'wheel_diameter': self.wheel_diameter,
            'tread_cof': self.wheel_friction,
            'drivetrain_motor': self.motor_type,
            'motors_per_side': self.motors_per_side,
            'gearbox_efficiency': self.gearbox_efficiency,
            'battery_nominal_voltage': self.battery_nominal_voltage,
            'battery_internal_resistance': self.battery_internal_resistance,
        }
        return 'robot:\n' + str(robot_parameters) + '\nmotor_curve:\n' + str(
            self.motor_curve)

    def get_motor_curve_data(self, motor_type='cim'):
        _motor_types = {
            'cim': 'motor_curves/cim-motor-curve-data-20151104.csv',
            'mini_cim': 'mini-cim-motor-curve-data-20151207.csv',
            '775pro': '775pro-motor-curve-data-20151208.csv',
            'bag': 'bag-motor-curve-data-20151207.csv'
        }

        try:
            curve_table = pd.read_csv(_motor_types[motor_type])
        except KeyError as e:
            raise e
        return curve_table

    def generate_motor_curve(self):
        motor_curve = self.get_motor_curve_data(motor_type=self.motor_type)

        ct = motor_curve

        motor_curve['speed'] = motor_curve['speed'] / 60.0

        motor_curve['total_current'] = motor_curve['current'] * self.motors
        motor_curve['battery_voltage'] = self.battery_voltage_under_load(
            motor_curve['total_current'])

        motor_curve['robot_max_pwm_allowed'] = self.max_pwm_allowed(
            motor_curve['total_current'])

        motor_curve['robot_velocity'] = self.robot_velocity(
            motor_curve['speed'])

        motor_curve['robot_acceleration'] = self.robot_acceleration(
            motor_curve['battery_voltage'], motor_curve['torque'],
            motor_curve['robot_max_pwm_allowed'])

        return motor_curve

    def battery_voltage_under_load(self, current):
        # V = I*R
        return self.battery_nominal_voltage - (
            current * self.battery_internal_resistance)

    def max_pwm_allowed(self, current):
        max_current = (
            self.battery_nominal_voltage - self.battery_min_allowed_voltage
        ) / self.battery_internal_resistance

        max_pwm = []
        for x in current:
            if max_current <= x:
                max_pwm.append(1 - ((x - max_current) / x))
            else:
                max_pwm.append(1)
        return max_pwm

    def wheel_torque(self, motor_voltage, motor_torque):
        motor_torque_voltage_corrected = motor_torque * (
            motor_voltage / self.curve_voltage)
        total_torque = motor_torque_voltage_corrected * self.motors_per_side * self.gear_ratio * self.gearbox_efficiency
        return total_torque

    def side_wheel_force(self, motor_voltage, motor_torque):
        # wheel_force = torque / distance
        wheel_force = self.wheel_torque(motor_voltage, motor_torque) / (
            self.wheel_diameter / 2)
        return wheel_force

    def total_wheel_force(self, motor_voltage, motor_torque):
        return self.side_wheel_force(motor_voltage, motor_torque) * 2

    def _acceleration(self, force):
        # acceleration = force / mass
        return force / self.mass

    def robot_acceleration(self, motor_voltage, motor_torque,
                           robot_max_pwm_allowed):
        return self._acceleration(
            self.total_wheel_force(motor_voltage, motor_torque) *
            robot_max_pwm_allowed)

    def robot_velocity(self, motor_velocity):
        return (motor_velocity / self.gear_ratio) * self.wheel_perimeter

    def find_max_pwm_allowed_equation(self):
        # Get everything that isnt being forced to 1
        x = self.motor_curve.loc[lambda df: df.robot_max_pwm_allowed < 1, :][
            'speed'].values
        y = self.motor_curve.loc[lambda df: df.robot_max_pwm_allowed < 1, :][
            'robot_max_pwm_allowed'].values

        # the transition point between limiting and not limiting
        transition = 0

        try:
            transition = x[::-1][0]
            coefs = poly.polyfit(x=x, y=y, deg=2)
            feq = poly.Polynomial(coefs)
            print('function for limiting drivetrain power')
            print('if motor_revolutions_per_second < {transition}:'.format(
                transition=transition))
            print(
                '    max_pwm = {0} + {1} * motor_revolutions_per_second + {2} * (motor_revolutions_per_second*motor_revolutions_per_second)'.
                format(coefs[0], coefs[1], coefs[2]))
            print('else:')
            print('    max_pwm = 1')
            print('return max_pwm')
            print(
                'piecewise transition point: {transition} motor_revolutions/second'.
                format(transition=transition))
            print(feq)
        except IndexError:
            # if we get an index error, it means that we do not need to limit power at any point on the curve. So, we set a pass-through function
            print('Yay! No need to limit power. You got lucky this time...')
            feq = lambda x: 1
            coefs = [0, 1, 0]
            x = [0]

        def max_pwm_allowed(speed):
            if speed < x[::-1][0]:
                return feq(speed)
            else:
                return 1

        the_list = []
        for s in self.motor_curve['speed'].values:
            the_list.append(max_pwm_allowed(s))

        self.motor_curve['robot_max_allowed_pwm_equation'] = the_list
        return max_pwm_allowed

    def find_voltage_limited_acceleration_equation(self):
        # get our x and y vectors
        x = self.motor_curve['speed'].values
        y = self.motor_curve['robot_acceleration'].values

        # get polynomials for best fit
        coefs = poly.polyfit(x=x, y=y, deg=3)

        # plot best fit
        geq = poly.Polynomial(coefs)
        self.motor_curve['robot_acceleration_fit'] = geq(
            self.motor_curve[['speed']])

        # pro-rate the physical acceleration 
        max_accel = self.motor_curve['robot_acceleration'].iloc[0]
        shift_amount = max_accel * self.reserve_acceleration
        coefs[0] = coefs[0] - shift_amount

        # turn polynomial coefficients into usable function
        feq = poly.Polynomial(coefs)

        # add calculated accelerations to motor curve for comparison
        self.motor_curve['robot_acceleration_targets'] = feq(
            self.motor_curve[['speed']])
        return feq


#class TankRobotController(object):
#    def __init__(self, window=20, step=0.1):
#        self.robot = TankRobot()
#        self.window = window
#        self.step = step
#
#    def __str__(self):
#        params = {'window': self.window, 'step': self.step}
#        return 'TankRobotController: {params}'.format(str(params))
#
#    def silly_controller(self, current_velocity, requested_velocity):
#        return 1

#    def generate_run(self, controller):
#        d = {}
#        current_velocity = 0
#        requested_velocity = 10 * 0.3048
#        d['commanded_power'] = []
#
#        for step in np.arange(0, self.window, self.step):
#            d['velocity'].append(current_velocity)
#            d['commanded_pwm'].append(
#                controller(current_velocity, requested_velocity))
#            d['robot_acceleration'].append(None)

#cim_curve = pd.read_csv(cim_csv)
#print(cim_curve)
#cim_curve.plot.line(x=0)

robot = TankRobot(
    gear_ratio=5.1,
    mass=134,
    battery_internal_resistance=0.011,
    battery_nominal_voltage=13.0,
    battery_min_allowed_voltage=6.5)
print(robot)
#robot.motor_curve.to_csv('test_data.csv')
robot.motor_curve[[
    'speed', 'robot_velocity', 'robot_acceleration', 'robot_acceleration_fit',
    'robot_acceleration_targets'
]].plot(x='speed')
robot.motor_curve[[
    'speed', 'robot_max_pwm_allowed', 'robot_max_allowed_pwm_equation'
]].plot(x='speed')
plt.show()

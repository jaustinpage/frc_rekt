# -*- coding: UTF-8 -*-
# pragma: no cover
import pytest

from frc_rekt.motor import Motor


@pytest.fixture(params=['cim', 'mini-cim', 'bag', '775pro'])
def motor_types(request):
    return request.param


def test_init(motor_types):
    """Test the creation of all motor types"""
    motor = Motor(motor_types)
    assert motor.motor_types == ['cim', 'mini-cim', '775pro', 'bag']
    assert motor._stall_voltages == [2, 4, 6, 8, 10, 12]
    assert motor._motor_curve_voltage == 12.0


@pytest.fixture
def motor(motor_types):
    return Motor(motor_types)


def test_generate_basic_function_current(motor):
    motor._generate_basic_function('current', plot=True)


def test_generate_basic_function_torque(motor):
    motor._generate_basic_function('torque', plot=True)


def test_get_voltage_scaled_current(motor):
    motor._gen_voltage_scaled_func('current', plot=True)


def test_get_voltage_scaled_torque(motor):
    motor._gen_voltage_scaled_func('torque', plot=True)

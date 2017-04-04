# -*- coding: UTF-8 -*-
# pylint: disable=missing-docstring, protected-access, redefined-outer-name
import pytest

from frc_rekt.motor import Motor


@pytest.fixture(params=['cim', 'mini-cim', 'bag', '775pro'])
def motor_types(request):
    return request.param


def test_init(motor_types):
    """Test the creation of all motor types"""
    Motor(motor_types)


@pytest.fixture
def motor(motor_types):
    return Motor(motor_types)


def test_get_voltage_scaled_current(motor):
    motor._gen_voltage_scaled_func('current', plot=True)


def test_get_voltage_scaled_torque(motor):
    motor._gen_voltage_scaled_func('torque', plot=True)

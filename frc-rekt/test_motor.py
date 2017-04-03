import pytest

from motor import Motor


@pytest.fixture(params=['cim', 'mini-cim', 'bag', '775pro'])
def motor_type(request):
    return request.param


# Make sure we can init before creating the motor generator
def test_init(motor_type):
    motor = Motor(motor_type)


@pytest.fixture
def motor(motor_type):
    return Motor(motor_type)


def test_get_voltage_scaled_current(motor):
    motor.generate_voltage_scaled_function('current', plot=True)


def test_get_voltage_scaled_torque(motor):
    motor.generate_voltage_scaled_function('torque', plot=True)

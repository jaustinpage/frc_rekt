# -*- coding: UTF-8 -*-
# pylint: disable=missing-docstring, protected-access, redefined-outer-name
import pytest

from frc_rekt.battery import Battery


def test_init():
    Battery()


@pytest.fixture
def battery():
    return Battery()


def test_voltage(battery):
    assert battery.voltage() == 13.2

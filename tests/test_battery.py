# -*- coding: UTF-8 -*-
import pytest

from frc_rekt.battery import Battery


def test_init():
    Battery()


@pytest.fixture
def battery():
    return Battery()


def test_voltage(battery):
    assert battery.voltage() == 13.2

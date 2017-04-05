# -*- coding: UTF-8 -*-
# pylint: disable=missing-docstring, protected-access, redefined-outer-name
import pytest

from frc_rekt.wheel import Wheel


def test_init():
    wheel = Wheel()
    assert wheel.diameter == 4
    assert wheel.cof == 1.3
    assert wheel.torque == 0.0
    assert wheel.force == 0.0


@pytest.fixture
def wheel():
    return Wheel()


def test_print(wheel):
    assert str(wheel) == 'Wheel(diameter=4.0, cof=1.3, torque=0.0)'

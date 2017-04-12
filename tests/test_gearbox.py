# -*- coding: UTF-8 -*-
import pytest

from frc_rekt.gearbox import Gearbox


def test_init():
    gearbox = Gearbox()
    assert gearbox.mechanical_advantage == 10.714285714285715


@pytest.fixture
def gearbox():
    return Gearbox()

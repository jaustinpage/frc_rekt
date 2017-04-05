# -*- coding: UTF-8 -*-
# pylint: disable=missing-docstring, protected-access, redefined-outer-name

import pytest

from frc_rekt.drivetrain import Drivetrain


def test_init():
    """Test the creation of a Drivetrain"""
    Drivetrain()


@pytest.fixture
def drivetrain():
    return Drivetrain()

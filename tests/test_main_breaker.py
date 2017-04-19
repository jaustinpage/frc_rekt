# -*- coding: UTF-8 -*-

import pytest

from frc_rekt.main_breaker import MainBreaker


def test_init():
    """Test the creation of main_breaker"""
    MainBreaker()


@pytest.fixture
def main_breaker():
    return MainBreaker()


def test_generate_functions(main_breaker):
    main_breaker._generate_functions(plot=True)


def test_public_functions(main_breaker):
    assert main_breaker.trip_time(240) == pytest.approx(
        (13.286548983982193, 34.401343327033658), rel=5e-5)

    assert main_breaker.temperature_derate(78) == pytest.approx(
        (0.97153542326750275, 1.2706642035856861), rel=5e-5)

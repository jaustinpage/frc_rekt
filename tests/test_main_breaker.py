# -*- coding: UTF-8 -*-
# pylint: disable=missing-docstring, protected-access, redefined-outer-name

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

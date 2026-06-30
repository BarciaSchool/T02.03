import doctest

from app import utils


def test_utils_doctests():
    resultado = doctest.testmod(utils, verbose=False)
    assert resultado.failed == 0

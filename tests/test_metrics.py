import pytest


from lagrangian_trajectory_clustering.metrics import (
    lcs_numpy,
    lcs_pure,
    lcs_numpy_numba,
    lcs_pure_numba,
)


@pytest.mark.parametrize(
    "lcs_func", [lcs_numpy, lcs_pure, lcs_numpy_numba, lcs_pure_numba]
)
def test_lcs(lcs_func):
    assert 3 == lcs_func("ABC", "_AB_C_")
    assert 1 == lcs_func("CBA", "_AB_C_")
    assert 0 == lcs_func("YYY", "XXX")
    assert 1 == lcs_func("__Y", "YYY")
    assert 0 == lcs_func("", "")

import pytest


from lagtrajclust.metrics import (
    lcs_numpy,
    lcs_pure,
    lcs_numpy_numba,
    lcs_pure_numba,
)


@pytest.mark.parametrize(
    "lcs_func", [lcs_numpy, lcs_pure, lcs_numpy_numba, lcs_pure_numba]
)
def test_lcs_numpy(lcs_func):
    assert 3 == lcs_func("ABC", "_AB_C_")
    assert 1 == lcs_func("CBA", "_AB_C_")
    assert 0 == lcs_func("YYY", "XXX")
    assert 1 == lcs_func("__Y", "YYY")
    assert 0 == lcs_func("", "")
    assert 4 == lcs_func((1, 2, 3, 4, 5), ("a", 2, 3, 4, 5))
    assert 0 == lcs_func("", ("a", 2, 3, 4, 5))
    assert 0 == lcs_func([], ("a", 2, 3, 4, 5))
    with pytest.raises(TypeError):
        lcs_func(1, ("a", 2, 3, 4, 5))


def test_lcs_pure():
    _lcs = lcs_pure
    assert 3 == _lcs("ABC", "_AB_C_")
    assert 1 == _lcs("CBA", "_AB_C_")
    assert 0 == _lcs("YYY", "XXX")
    assert 1 == _lcs("__Y", "YYY")
    assert 0 == _lcs("", "")
    assert 4 == _lcs((1, 2, 3, 4, 5), ("a", 2, 3, 4, 5))
    assert 0 == _lcs("", ("a", 2, 3, 4, 5))
    assert 0 == _lcs([], ("a", 2, 3, 4, 5))
    with pytest.raises(TypeError):
        _lcs(1, ("a", 2, 3, 4, 5))

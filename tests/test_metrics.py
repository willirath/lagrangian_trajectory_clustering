import pytest


from string import ascii_uppercase
import random


from lagrangian_trajectory_clustering.metrics import (
    lcs_numpy,
    lcs_numpy_numba,
    lcs_pure,
    lcs_pure_numba,
    levenshtein_numpy,
    levenshtein_numpy_numba,
)


@pytest.mark.parametrize(
    "lcs_implementation", [lcs_numpy, lcs_pure, lcs_numpy_numba, lcs_pure_numba]
)
def test_lcs(lcs_implementation):
    assert 3 == lcs_implementation("ABC", "_AB_C_")
    assert 1 == lcs_implementation("CBA", "_AB_C_")
    assert 0 == lcs_implementation("YYY", "XXX")
    assert 1 == lcs_implementation("__Y", "YYY")
    assert 0 == lcs_implementation("", "")


@pytest.mark.parametrize("lcs_pure_implementation", [lcs_pure, lcs_pure_numba])
@pytest.mark.parametrize("lcs_numpy_implementation", [lcs_numpy, lcs_numpy_numba])
def test_lcs_implementations_back_to_back(
    lcs_pure_implementation, lcs_numpy_implementation
):
    """Compare alternative implementations of LCS."""
    num_runs = 10
    max_sequence_length = 100
    for run in range(num_runs):
        x = "".join(
            random.choice(ascii_uppercase)
            for n in range(random.randint(1, max_sequence_length))
        )
        y = "".join(
            random.choice(ascii_uppercase)
            for n in range(random.randint(1, max_sequence_length))
        )
        assert lcs_pure_implementation(x, y) == lcs_numpy_implementation(x, y)


@pytest.mark.parametrize(
    "levenshtein_implementation", [levenshtein_numpy, levenshtein_numpy_numba]
)
def test_levenshtein(levenshtein_implementation):
    assert 3 == levenshtein_implementation("kitten", "sitting")
    assert 0 == levenshtein_implementation("abcde", "abcde")

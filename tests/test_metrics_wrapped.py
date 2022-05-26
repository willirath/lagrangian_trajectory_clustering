import pytest

from lagrangian_trajectory_clustering.metrics import (
    lcs_numpy,
    lcs_numpy_numba,
    lcs_pure,
    lcs_pure_numba,
    levenshtein_numpy,
    levenshtein_numpy_numba,
)

from lagrangian_trajectory_clustering.metrics_wrapped import wrapped_metric


@pytest.mark.parametrize("normalize", [True, False])
@pytest.mark.parametrize(
    "lcs_implementation", [lcs_numpy, lcs_numpy_numba, lcs_pure, lcs_pure_numba]
)
def test_wrapped_lcs(lcs_implementation, normalize):
    sequences = [
        "ABCDEFG",
        "ABCDE__",
        "ABC__FG",
    ]
    lcs_wrapped = wrapped_metric(
        metric_function=lcs_implementation,
        sequences_mapping=sequences,
        normalize=normalize,
    )
    if normalize:
        assert 5 / 7 == lcs_wrapped([0], [1])
        assert 5 / 7 == lcs_wrapped([0], [2])
        assert 5 / 7 == lcs_wrapped([1], [2])
    else:
        assert 5 == lcs_wrapped([0], [1])
        assert 5 == lcs_wrapped([0], [2])
        assert 5 == lcs_wrapped([1], [2])


@pytest.mark.parametrize("normalize", [True, False])
@pytest.mark.parametrize(
    "levenshtein_implementation", [levenshtein_numpy, levenshtein_numpy_numba]
)
def test_wrapped_levenshtein(levenshtein_implementation, normalize):
    sequences = [
        "ABCDEFG",
        "ABCDE__",
        "ABC__FG",
    ]
    levenshtein_wrapped = wrapped_metric(
        metric_function=levenshtein_implementation,
        sequences_mapping=sequences,
        normalize=normalize,
    )
    if normalize:
        assert 2 / 7 == levenshtein_wrapped([0], [1])
        assert 2 / 7 == levenshtein_wrapped([0], [2])
        assert 4 / 7 == levenshtein_wrapped([1], [2])
    else:
        assert 2 == levenshtein_wrapped([0], [1])
        assert 2 == levenshtein_wrapped([0], [2])
        assert 4 == levenshtein_wrapped([1], [2])

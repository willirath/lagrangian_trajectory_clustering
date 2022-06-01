import pandas as pd

from lagrangian_trajectory_clustering.trafo.sequence import (
    remove_subsequent_identical_elements,
)


def test_remove_subsequent_identical_elements_preserves_index():
    series = pd.Series(
        [
            ["a", "a", "b", "b", "c", "d"],
            ["a", "b", "c", "c", "d"],
        ],
        index=[0, 1],
    )
    processed_series = remove_subsequent_identical_elements(series)
    assert all(a == b for a, b in zip(series.index, processed_series.index))


def test_remove_subsequent_identical_elements_removes_dupes():
    series = pd.Series(
        [
            ["a", "a", "b", "b", "c", "d", "a"],
            ["a", "b", "c", "c", "d"],
        ],
        index=[0, 1],
    )
    processed_series = remove_subsequent_identical_elements(series)
    assert all(
        a == b for a, b in zip(processed_series.loc[0], ["a", "b", "c", "d", "a"])
    )
    assert all(a == b for a, b in zip(processed_series.loc[1], ["a", "b", "c", "d"]))

from audioop import mul

import pandas as pd

from lagrangian_trajectory_clustering.trafo.sequence import (
    multi_index_series_to_series_sequences,
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


def test_series_to_series_of_sequences_default_grouping():
    original = pd.Series(
        ["a", "b", "c", "a", "b"],
        index=pd.MultiIndex.from_tuples(
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)], names=["traj", "obs"]
        ),
    )
    processed = multi_index_series_to_series_sequences(original)
    assert all(a == b for a, b in zip(processed.index, [0, 1]))
    assert all(a == b for a, b in zip(processed.loc[0], ["a", "b", "c"]))
    assert all(a == b for a, b in zip(processed.loc[1], ["a", "b"]))


def test_series_to_series_of_sequences_explicit_grouping():
    original = pd.Series(
        ["a", "b", "c", "a", "b"],
        index=pd.MultiIndex.from_tuples(
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)], names=["traj", "obs"]
        ),
    )
    processed = multi_index_series_to_series_sequences(original, groupby="traj")
    assert all(a == b for a, b in zip(processed.index, [0, 1]))
    assert all(a == b for a, b in zip(processed.loc[0], ["a", "b", "c"]))
    assert all(a == b for a, b in zip(processed.loc[1], ["a", "b"]))

import numpy as np


def get_step_sizes(df):
    """Diagnose all step sizes along trajectories.

    Parameters
    ----------
    df: pandas.Dataframe
        Contains columns "longitude" and "latitude".

    Returns
    -------
    pandas.Series
        Contains step sizes in meters.

    """
    step_lengths_meters = (
        111e3
        * (
            df.groupby("traj")["latitude"].diff() ** 2
            + (
                df.groupby("traj")["longitude"].diff()
                * np.cos(np.deg2rad(df["latitude"]))
            )
            ** 2
        )
        ** 0.5
    )
    # replace 0 and drop invalids
    step_lengths_meters = step_lengths_meters.replace({0: np.nan}).dropna()
    return step_lengths_meters


def _get_non_repeating_sequence(sequence):
    sequence = iter(sequence)
    current = next(sequence)
    # always yield first element
    yield current
    for new in sequence:
        # only yield next element if it's different
        if new != current:
            yield new
            current = new


def remove_subsequent_identical_elements(series):
    """From a series of ordered collections, remove subsequent dupes.

    Parameters
    ----------
    series: pandas.Series
        Each element contains a list or other ordered collection of elements.

    Returns
    -------
    pandas.Series
        Same as input but with subsequent dupes removed.

    """
    return series.apply(_get_non_repeating_sequence).apply(list)


def multi_index_series_to_series_sequences(series=None, groupby=None):
    """Turn a series with a multi-index into a series of lists of elements.

    Parameters
    ----------
    series: pandas.Series
        Each element contains a single element.
    groupby: sequence
        Optional. Will be used to group the series. If it's not given, the level 0
        of the index ofseries will be used to group.

    Returns
    -------
    pandas.Series:
        Each element contains an ordered collection (list) of elements.

    """
    if groupby is None:
        groupby = series.index.get_level_values(0)
    return series.groupby(groupby).apply(list)

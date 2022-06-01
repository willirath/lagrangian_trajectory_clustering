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

import numpy as np
from functools import reduce
from operator import add


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


def series_sequences_to_multi_index_series(series=None, index_name="obs"):
    """Turn a series of iterables into a multi-index series.

    Parameters
    ----------
    series: pandas.Series
        Each element contains an iterable.
    index_name: str
        Name of the additional index level.

    Returns
    -------
    pandas.Series:
        Multi-index series where each element contains a single element.

    """
    additional_index_column = (
        series.apply(lambda lst: list(range(len(lst)))).rename(index_name).explode()
    )
    return (
        series.explode()
        .to_frame()
        .set_index(additional_index_column, append=True)
        .iloc[:, 0]
    )


def _line_between(start, end):
    """Find intermediate points on a line from (x0, y0) to (x1, y1).
    
    Parameters
    ----------
    start: tuple
        Contains x0 and y0.
    end: tuple
        Contains x1 and y1.
    
    Returns
    -------
    list
        List of all intermediate points (x, y).
    
    """
    x0, y0 = start
    x1, y1 = end
    N = max(abs(x1 - x0) + 1, abs(y1 - y0) + 1)
    dx = (x1 - x0) / (N - 1)
    dy = (y1 - y0) / (N - 1)
    xx = (round(x0 + n * dx) for n in range(N))
    yy = (round(y0 + n * dy) for n in range(N))
    return list(zip(xx, yy))


def _line_between_segments(points):
    """Fill in lines on all segments of points.
    
    Parameters
    ----------
    points: list
        List of points (x, y).
        
    Returns
    -------
    list
        List of points (x, y) with all segments filled in.

    """
    segments = [
        _line_between(start, end)[:-1] for start, end in zip(points[:-1], points[1:])
    ] + [points[-1:],]
    return reduce(add, segments)


def fill_in_segments(series):
    """Fill in all intermediate points.

    Parameters
    ----------
    series: pandas.Series
        Each element contains an iterable of points along a trajectory.

    Returns
    -------
    pandas.Series:
        Each element contains an iterable of points along a trajectory.

    """
    return series.apply(_line_between_segments)

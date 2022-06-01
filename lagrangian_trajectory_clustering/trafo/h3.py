import h3
import numpy as np
import pandas as pd


def find_max_needed_h3_resolution(df, quantile=0.5):
    """Estimate the max. meaningful h3 resolution for the given data.

    This will find the smallest stepsize in the data and return the highest
    h3 resolution needed to resolve this stepsize. This stepsize is diagnosed as the
    median of all steps.

    Parameters
    ----------
    df: pandas.Dataframe
        Contains columns "longitude" and "latitude".
    quantile: float
        Quantile to be used for the definition of the typical step size.
        Defaults to 0.5 (the median).

    Returns
    -------
    int
        Max. needed h3 resolution level.

    See https://h3geo.org/docs/core-library/restable/
    """
    # dirty but good enough step length estimate
    step_lengths_meters = get_step_sizes(df)
    typical_step_length_meters = step_lengths_meters.quantile(quantile)
    h3_lengths_meters = [(h3.hex_area(res) ** 0.5) * 1e3 for res in range(0, 16)]
    max_needed_resolution = sum(
        h3l > typical_step_length_meters for h3l in h3_lengths_meters
    )
    return max_needed_resolution


def add_max_res_h3_column(df, max_res=15):
    """Add a column containing the max. resolution h3 cell.

    Parameters
    ----------
    df: pandas.Dataframe
        Has columns "latitude" and "longitude".
    max_res: int
        Max resolution needed. Defaults to 15 (which is the max.
        possible h3 resolution of approx. 0.5 meters)

    Returns
    -------
    pandas.Dataframe
        Same as input with additional column "h3maxres" containing the max. resolution h3 cell id.

    """
    df["h3maxres"] = df.apply(
        lambda rw: h3.geo_to_h3(
            lat=rw["latitude"],
            lng=rw["longitude"],
            resolution=max_res,
        ),
        axis=1,
    )

    return df


def h3_series_to_h3_parent(h3_series, resolution=0):
    """Convert a df with h3 cell ids to a coarser resolution.

    Parameters
    ----------
    h3_series: pandas.Dataframe
        Has column "h3".
    resolution: int
        H3 resolution. Default to 0 corresponding to approx. 1000 kilometers.
        See: https://h3geo.org/docs/core-library/restable/

    Returns
    -------
    pandas.Series
        h3s
    """
    return h3_series.apply(lambda cellid: h3.h3_to_parent(cellid, resolution))


def h3_series_to_series_of_h3_sequences(h3_series=None, groupby=None):
    """Turn a series of H3s into a series of lists of H3s.

    Parameters
    ----------
    h3_series: pandas.Series
        Each element contains a single h3.
    groupby: sequence
        Optional. Will be used to group the h3s. If it's not given, the level 0
        of the index of h3_series will be used to group.

    Returns
    -------
    pandas.Series:
        Each element contains an ordered collection (list) of h3s.

    """
    if groupby is None:
        groupby = h3_series.index.get_level_values(0)
    return h3_series.groupby(groupby).apply(list)


def _get_h3_line_between(sequence):
    sequence = iter(sequence)
    last = next(sequence)
    for new in sequence:
        for h3line in list(h3.h3_line(last, new))[:-1]:
            yield h3line
        last = new
    yield last


def fill_in_h3_gaps(h3_series):
    """In a series of ordered collections of H3s, fill in the gaps.

    Uses h3_line.

    Parameters
    ----------
    h3_series: pandas.Series
        Each element contains a list or other ordered collection of H3s.

    Returns
    -------
    pandas.Series
        Same as input but with gaps between subsequent elements filled.

    """
    return h3_series.apply(_get_h3_line_between).apply(list)


def h3_sequences_to_series(h3_sequences):
    """Turn a sequence of H3s into a pandas series.

    Parameters
    ----------
    h3_sequences: pandas.Series
        Each element contains an ordered collection of H3s.

    Returns
    -------
    pandas.Series
        Each element contains a separate H3. To enumerate the elements fo the
        original ordered collections, there will be an additional index level
        called 'obs'.

    """
    obs = h3_sequences.apply(lambda lst: list(range(len(lst)))).explode().rename("obs")
    h3_series = h3_sequences.explode(ignore_index=False)
    traj = h3_series.index
    return h3_series.reset_index().set_index([traj, obs])


def h3_to_geo(h3_series):
    return pd.DataFrame(
        h3_series.apply(h3.h3_to_geo).values.tolist(),
        columns=["latitude", "longitude"],
    ).set_index(h3_series.index)

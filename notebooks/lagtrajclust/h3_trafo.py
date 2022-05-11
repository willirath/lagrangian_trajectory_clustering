import pandas as pd
import numpy as np

import h3
import h3.api.numpy_int
import h3.api.basic_str


def df_to_h3(df, resolution=8):
    """Convert series of latitude and longitude to series of h3s.
    
    Parameters
    ----------
    df: pandas.Dataframe
        Has columns "latitude" and "longitude".
    resolution: int
        H3 resolution. Default to 8 corresponding to approx. 500 meters.
        See: https://h3geo.org/docs/core-library/restable/
        
    Returns
    -------
    pandas.Series
        h3s
    """
    return df.apply(
        lambda rw: h3.geo_to_h3(
            lat=rw["latitude"], lng=rw["longitude"], resolution=resolution,
        ),
        axis=1,
    ).to_frame(name="h3")


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


def h3_series_to_series_of_h3_sequences(h3_series):
    return h3_series.groupby(h3_series.index.get_level_values(0)).apply(list)


def _get_non_repeating_sequence(sequence):
    sequence = iter(sequence)
    current = next(sequence)
    yield current  # always return first element
    for new in sequence:
        if new != current:
            yield new
            current = new


def remove_subsequent_identical_elements(h3_series):
    return h3_series.apply(_get_non_repeating_sequence).apply(list)


def transform_unique_transitions(h3_sequence):
    return list(
        filter(lambda se: se[0] != se[1], zip(h3_sequence[:-1], h3_sequence[1:]))
    )

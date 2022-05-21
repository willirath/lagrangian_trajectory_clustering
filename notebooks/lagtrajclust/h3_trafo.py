import pandas as pd
import numpy as np

import h3
import h3.api.numpy_int
import h3.api.basic_str


def _get_step_sizes(df):
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
    step_lengths_meters = _get_step_sizes(df)
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
            lat=rw["latitude"], lng=rw["longitude"], resolution=max_res,
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

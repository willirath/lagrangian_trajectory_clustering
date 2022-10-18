import numpy as np
import pandas as pd


def geo_df_to_grid_series(
    geo_df=None,
    lat_start=-90,
    lat_end=90,
    lat_num=181,
    lon_start=0,
    lon_end=360,
    lon_num=361,
):
    """Transform geo df to grid index tuples.

    Parameters
    ----------
    geo_df: pandas.DataFrame
        Has columns "longitude" and "latitude".
    lat_start: float
        Left edge of leftmost lat bin. Defaults to -90.
    lat_end: float
        Left edge of leftmost lat bin. Defaults to 90.
    lat_num: int
        Number of lat bin _edges_. Defaults to 181.
    lon_start: float
        Left edge of leftmost lon bin. Defaults to 0.
    lon_end: float
        Left edge of leftmost lon bin. Defaults to 360.
    lon_num: int
        Number of lon bin _edges_. Defaults to 361.

    Returns
    -------
    pandas.Series
        Series of (longitude, latitude) index tuples. Has the same index as geo_df.

    """
    lon_bins = np.linspace(lon_start, lon_end, lon_num)
    lat_bins = np.linspace(lat_start, lat_end, lat_num)
    lon_index = np.digitize(geo_df["longitude"] % 360, lon_bins) - 1
    lat_index = np.digitize(geo_df["latitude"], lat_bins) - 1
    return pd.Series(
        zip(lon_index, lat_index), index=geo_df.index, name="grid_index_lon_lat"
    )


def grid_series_to_geo_df(
    grid_series=None,
    lat_start=-90,
    lat_end=90,
    lat_num=181,
    lon_start=0,
    lon_end=360,
    lon_num=361,
):
    """Transform grid index tuples to geo dataframe.

    Parameters
    ----------
    grid_series: pandas.Series
        Elements are (lon, lat) tuples.
    lat_start: float
        Left edge of leftmost lat bin. Defaults to -90.
    lat_end: float
        Left edge of leftmost lat bin. Defaults to 90.
    lat_num: int
        Number of lat bin _edges_. Defaults to 181.
    lon_start: float
        Left edge of leftmost lon bin. Defaults to 0.
    lon_end: float
        Left edge of leftmost lon bin. Defaults to 360.
    lon_num: int
        Number of lon bin _edges_. Defaults to 361.

    Returns
    -------
    pandas.DataFrame
        Has columns "longitude" and "latitude". Has the same index as grid_series.

    """
    dlon = (lon_end - lon_start) / (lon_num - 1)
    dlat = (lat_end - lat_start) / (lat_num - 1)
    geo_df = pd.DataFrame(
        {
            "longitude": list(
                lon_start + (0.5 + grid_series.apply(lambda t: t[0])) * dlon
            ),
            "latitude": list(
                lat_start + (0.5 + grid_series.apply(lambda t: t[1])) * dlat
            ),
        },
        index=grid_series.index,
    )
    return geo_df

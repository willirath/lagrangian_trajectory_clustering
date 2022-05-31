from lagrangian_trajectory_clustering.trafo.grid import (
    geo_df_to_grid_series,
    grid_series_to_geo_df,
)

import pandas as pd


def test_geo_to_grid():
    """Test that traf from geo to grid indices works as expected."""
    traj_df = pd.DataFrame(
        {"longitude": [-11.1, 12.3, 45.1], "latitude": [-80.5, 70.4, 53.1],},
        index=[0, 1, 2,],
    )
    grid_series = geo_df_to_grid_series(
        traj_df,
        lat_start=-90,
        lat_end=90,
        lat_num=181,
        lon_start=0,
        lon_end=360,
        lon_num=361,
    )
    true_lon_indices = [348, 12, 45]
    true_lat_indices = [9, 160, 143]
    test_lon_indices = list(grid_series.apply(lambda t: t[0]))
    test_lat_indices = list(grid_series.apply(lambda t: t[1]))
    assert all(a == b for a, b in zip(true_lon_indices, test_lon_indices))
    assert all(a == b for a, b in zip(true_lat_indices, test_lat_indices))


def test_grid_to_geo():
    """Test that trafo from grid indices to geo works as expexted."""
    traj_df = pd.DataFrame(
        {"longitude": [-11.1, 12.3, 45.1], "latitude": [-80.5, 70.4, 53.1],},
        index=[0, 1, 2,],
    )
    grid_series = geo_df_to_grid_series(
        traj_df,
        lat_start=-90,
        lat_end=90,
        lat_num=181,
        lon_start=0,
        lon_end=360,
        lon_num=361,
    )
    geo_df = grid_series_to_geo_df(
        grid_series,
        lat_start=-90,
        lat_end=90,
        lat_num=181,
        lon_start=0,
        lon_end=360,
        lon_num=361,
    )
    true_lon_values = [348.5, 12.5, 45.5]
    true_lat_values = [-80.5, 70.5, 53.5]
    test_lon_values = list(geo_df["longitude"])
    test_lat_values = list(geo_df["latitude"])
    print(test_lat_values)
    assert all(a == b for a, b in zip(true_lon_values, test_lon_values))
    assert all(a == b for a, b in zip(true_lat_values, test_lat_values))


def test_geo_to_grid_idempotency():
    """Test that repeated application of the grid trafo does not change results."""
    traj_df = pd.DataFrame(
        {"longitude": [-11.1, 12.3, 45.1], "latitude": [-80.5, 70.4, 53.1],},
        index=[0, 1, 2,],
    )
    grid_series_0 = geo_df_to_grid_series(
        traj_df,
        lat_start=-90,
        lat_end=90,
        lat_num=181,
        lon_start=0,
        lon_end=360,
        lon_num=361,
    )
    _geo_df = grid_series_to_geo_df(
        grid_series_0,
        lat_start=-90,
        lat_end=90,
        lat_num=181,
        lon_start=0,
        lon_end=360,
        lon_num=361,
    )
    grid_series_1 = geo_df_to_grid_series(
        _geo_df,
        lat_start=-90,
        lat_end=90,
        lat_num=181,
        lon_start=0,
        lon_end=360,
        lon_num=361,
    )
    test_lon_indices_0 = list(grid_series_0.apply(lambda t: t[0]))
    test_lat_indices_0 = list(grid_series_0.apply(lambda t: t[1]))
    test_lon_indices_1 = list(grid_series_1.apply(lambda t: t[0]))
    test_lat_indices_1 = list(grid_series_1.apply(lambda t: t[1]))
    assert all(a == b for a, b in zip(test_lon_indices_0, test_lon_indices_1))
    assert all(a == b for a, b in zip(test_lat_indices_0, test_lat_indices_1))

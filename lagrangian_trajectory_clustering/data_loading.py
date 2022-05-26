from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from pooch import retrieve


def load_medsea_trajectories(cache_path="data/"):
    """Load Med Sea trajectories from https://doi.org/10.5281/zenodo.4650317

    Parameters
    ----------
    cache_path: str or pathlike
        Path to the cache dir. Defaults to "data/".

    Returns
    -------
    pandas.DataFrame
        All trajectories in dataset.
    """
    file_name = retrieve(
        url="https://zenodo.org/record/4650317/files/trajectories_nostokes_subset_10000.csv.gz",
        path=cache_path,
        known_hash="605e422d5fb18b0379ab1d8f0f4f2e79c142d07270f20db609fd4261d4a4f1fe",
    )

    df = pd.read_csv(file_name)[["traj", "obs", "time", "lat", "lon"]]
    df["time"] = pd.to_datetime(df["time"])

    df = df.set_index(["traj", "obs"])

    df = df.sort_index(axis=0, level=0)

    # make sure cols are called latitude and longitude
    df = df.rename(columns={"lat": "latitude", "lon": "longitude"})

    return df


def load_labsea_trajectories(cache_path="data/"):
    """Load lab sea data from http://hdl.handle.net/20.500.12085/830c72af-b5ca-44ac-8357-3173392f402b

    Parameters
    ----------
    cache_path: str or pathlike
        Path to the cache dir. Defaults to "data/".

    Returns
    -------
    pandas.DataFrame
        All trajectories in dataset.
    """
    file_name = (
        Path(cache_path) / "tracks_randomvel_mxl_osnap_backwards_1990_10000trajs.csv"
    )
    if not file_name.exists():
        ds = xr.open_zarr(
            "https://data.geomar.de/downloads/20.500.12085/830c72af-b5ca-44ac-8357-3173392f402b/submitted/tracks_randomvel_mxl_osnap_backwards_1990.zarr/"
        )
        df = (
            ds[
                [
                    "lat",
                    "lon",
                    "time",
                ]
            ]
            .isel(traj=slice(0, 10_000))
            .to_dataframe()
        )

        df = df.reset_index()
        df.to_csv(file_name, index=False)
    else:
        df = pd.read_csv(file_name)

    df = df.set_index(["traj", "obs"])
    df = df.sort_index(axis=0, level=0)

    # make sure cols are called latitude and longitude
    df = df.rename(columns={"lat": "latitude", "lon": "longitude"})

    return df


def subset_trajectories(
    df=None,
    num_traj=300,
    use_random=False,
    random_seed=None,
):
    """Subset trajectory data.

    Parameters
    ----------
    df: dataframe
        Data frame to subset.
    num_traj: int
        Number of trajectories to load
    use_random: bool
        If True, choose num_traj trajectories at random.
        If False, choose first num_traj trajectories.
    random_seed: int
        Optional seed for the RNG used to select random trajectories.

    Returns
    -------
    pandas.DataFrame
        Trajectories

    """
    # the whole dataset is too big to open here.
    traj_series = df.reset_index()["traj"]
    if use_random:
        if random_seed is not None:
            np.random.seed(random_seed)
        # Let's subset to fewer random trajectories:
        random_trajs = np.random.choice(np.unique(traj_series), num_traj, replace=False)
        traj_mask = traj_series.apply(lambda x: x in random_trajs)
    else:
        # Let's use the first N trajectories
        first_n_trajs = np.unique(traj_series)[:num_traj]
        traj_mask = traj_series.apply(lambda x: x in first_n_trajs)

    df = df.reset_index()[traj_mask].set_index(["traj", "obs"])

    return df

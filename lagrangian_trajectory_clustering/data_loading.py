from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from pooch import retrieve


def load_cape_verde_trajectories(year=1993, cache_path="data/"):
    """Load Cape Verde trajectories from https://doi.org/10.5281/zenodo.6589933

    Parameters
    ----------
    year: int
        Year to load from. There are data for 1993..2017 available.
        Defaults to 1993.
    cache_path: str or pathlike
        Path to the cache dir. Defaults to "data/".

    Returns
    -------
    pandas.DataFrame
        All trajectories in dataset.
    """
    hashes = {
        "cape_verde_drift_trajectories_1-10000_1993.csv.gz": "md5:ef56bc1dcf83d2dfa85f815fe4902d82",
        "cape_verde_drift_trajectories_1-10000_1994.csv.gz": "md5:6e4d07f018294224b4c3a26092bb8e27",
        "cape_verde_drift_trajectories_1-10000_1995.csv.gz": "md5:2ab1f9ffc881de0c21fcade2c12010ee",
        "cape_verde_drift_trajectories_1-10000_1996.csv.gz": "md5:800a2f5b9cd8b7e56c75ce15a7363dca",
        "cape_verde_drift_trajectories_1-10000_1997.csv.gz": "md5:d967eeceacf4d7c3630c1d396f0affc4",
        "cape_verde_drift_trajectories_1-10000_1998.csv.gz": "md5:d21f7509aca7c5aaba17415ba6b9b9d9",
        "cape_verde_drift_trajectories_1-10000_1999.csv.gz": "md5:38fc6fe5ddd598cc7ae9b55d6db01711",
        "cape_verde_drift_trajectories_1-10000_2000.csv.gz": "md5:a320405ac2d4d28349f5f4bfe43073ed",
        "cape_verde_drift_trajectories_1-10000_2001.csv.gz": "md5:ec7f77fab7c70e87783a6359623c93b8",
        "cape_verde_drift_trajectories_1-10000_2002.csv.gz": "md5:16b66f837b8f4e831c1ad72bc513195b",
        "cape_verde_drift_trajectories_1-10000_2003.csv.gz": "md5:8a4ce9ea4e4ed443b4dd9d590846f7b5",
        "cape_verde_drift_trajectories_1-10000_2004.csv.gz": "md5:66f4f7b7db774f96dfc82739537efc94",
        "cape_verde_drift_trajectories_1-10000_2005.csv.gz": "md5:479b330f464042ec7513be0fcda1bfed",
        "cape_verde_drift_trajectories_1-10000_2006.csv.gz": "md5:28b6054fbe7fef5a132cb5e8294088c8",
        "cape_verde_drift_trajectories_1-10000_2007.csv.gz": "md5:20e82326107a5924413829d4e6ed70e3",
        "cape_verde_drift_trajectories_1-10000_2008.csv.gz": "md5:6ac0c56c635908c77a974b2ce9bdcd8b",
        "cape_verde_drift_trajectories_1-10000_2009.csv.gz": "md5:b19d1c17b04a3557bbaef737b1dc6f32",
        "cape_verde_drift_trajectories_1-10000_2010.csv.gz": "md5:1701e3b84dc783c9b9f1451b0fa531ff",
        "cape_verde_drift_trajectories_1-10000_2011.csv.gz": "md5:31279ba8b032b5f7607e90b4c01053ab",
        "cape_verde_drift_trajectories_1-10000_2012.csv.gz": "md5:3cd0a5e6ac37b469e6f11c1dc402103b",
        "cape_verde_drift_trajectories_1-10000_2013.csv.gz": "md5:2f145489bc9dcd358c34689292cf5122",
        "cape_verde_drift_trajectories_1-10000_2014.csv.gz": "md5:23d2d43aa57c83a9597cef8bd4e4642d",
        "cape_verde_drift_trajectories_1-10000_2015.csv.gz": "md5:9054f7b6c82a4ebfd371d9a0e6c63f06",
        "cape_verde_drift_trajectories_1-10000_2016.csv.gz": "md5:f1346b82079dec8099c89113a7678c2b",
        "cape_verde_drift_trajectories_1-10000_2017.csv.gz": "md5:67300c5de652b6e00373e5ebad59ecf4",
    }
    key = f"cape_verde_drift_trajectories_1-10000_{year:04d}.csv.gz"
    file_name = retrieve(
        url=f"doi:10.5281/zenodo.6589933/{key}",
        path=cache_path,
        known_hash=hashes[key],
    )

    df = pd.read_csv(file_name)[["traj", "obs", "time", "lat", "lon"]]
    df["time"] = pd.to_datetime(df["time"])

    df = df.set_index(["traj", "obs"])

    df = df.sort_index(axis=0, level=0)

    # make sure cols are called latitude and longitude
    df = df.rename(columns={"lat": "latitude", "lon": "longitude"})

    return df


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
        df = ds[["lat", "lon", "time",]].isel(traj=slice(0, 10_000)).to_dataframe()

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
    df=None, num_traj=300, use_random=False, random_seed=None,
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

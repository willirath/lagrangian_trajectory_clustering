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
        "cape_verde_drift_trajectories_1-10000_1993.csv.gz": "md5:5615e96a199058b2b2a1b1c6a81fa658",
        "cape_verde_drift_trajectories_1-10000_1994.csv.gz": "md5:6274b95fa22067d905609fb60cc37f0b",
        "cape_verde_drift_trajectories_1-10000_1995.csv.gz": "md5:220905092b6bbb362faf36de14e15666",
        "cape_verde_drift_trajectories_1-10000_1996.csv.gz": "md5:bc89aef5400772be961c5643af4645a5",
        "cape_verde_drift_trajectories_1-10000_1997.csv.gz": "md5:4014832ec372c39809d83c897588e86b",
        "cape_verde_drift_trajectories_1-10000_1998.csv.gz": "md5:0c4868543b137c88bfd396ad8e290d10",
        "cape_verde_drift_trajectories_1-10000_1999.csv.gz": "md5:0cb004599536102ba472de5b8137636e",
        "cape_verde_drift_trajectories_1-10000_2000.csv.gz": "md5:a0276a0289059a983a0991af269f302c",
        "cape_verde_drift_trajectories_1-10000_2001.csv.gz": "md5:f66f388159a3d9bcb517887f2dda15f7",
        "cape_verde_drift_trajectories_1-10000_2002.csv.gz": "md5:61e2a8e509df5a3ea5e4d23563723844",
        "cape_verde_drift_trajectories_1-10000_2003.csv.gz": "md5:95a512c4378cafb6c6c2f2a677cea609",
        "cape_verde_drift_trajectories_1-10000_2004.csv.gz": "md5:bcfe219f01d1e079299b649acd06d4e2",
        "cape_verde_drift_trajectories_1-10000_2005.csv.gz": "md5:cf85cc276ccc5b96f18adfdf3eb041b0",
        "cape_verde_drift_trajectories_1-10000_2006.csv.gz": "md5:e414f66aca25f1a9e7299d0cab160ced",
        "cape_verde_drift_trajectories_1-10000_2007.csv.gz": "md5:652170fbff78331d374db1cb1b4f711a",
        "cape_verde_drift_trajectories_1-10000_2008.csv.gz": "md5:e81bd041b921151fe4db5d3e314c4d43",
        "cape_verde_drift_trajectories_1-10000_2009.csv.gz": "md5:92c51bc9f3506f6748e22a6487a2a3fc",
        "cape_verde_drift_trajectories_1-10000_2010.csv.gz": "md5:77b9c8858ebc9b09769a41afd5dee712",
        "cape_verde_drift_trajectories_1-10000_2011.csv.gz": "md5:c460e2951915610d3bf25e61f47ee5a9",
        "cape_verde_drift_trajectories_1-10000_2012.csv.gz": "md5:9efa8ff855fc814e13dfcfb05cf3abf8",
        "cape_verde_drift_trajectories_1-10000_2013.csv.gz": "md5:82c763b8c89c8bc7d0c7cd4d856111e5",
        "cape_verde_drift_trajectories_1-10000_2014.csv.gz": "md5:386e2b9912952f0d1ec4cc22e93416fc",
        "cape_verde_drift_trajectories_1-10000_2015.csv.gz": "md5:8345338f098b0556010fb855d71e8508",
        "cape_verde_drift_trajectories_1-10000_2016.csv.gz": "md5:2b2783e552a5125f9a70d5675d372c30",
        "cape_verde_drift_trajectories_1-10000_2017.csv.gz": "md5:33d7e557d9f35abd262f349bb6c38bb7",
    }
    key = f"cape_verde_drift_trajectories_1-10000_{year:04d}.csv.gz"
    file_name = retrieve(
        url=f"doi:10.5281/zenodo.6826071/{key}",
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
        url="doi:10.5281/zenodo.4650317/trajectories_nostokes_subset_10000.csv.gz",
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

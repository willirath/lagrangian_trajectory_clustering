import pandas as pd
import numpy as np


def load_and_subset_trajectories_csv(
    file_name, num_traj=300, use_random=False, random_seed=None,
):
    """Load data file and extract a number of trajectories.
    
    Parameters
    ----------
    file_name: str or Path
        File to open.
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
    df = pd.read_csv(file_name)

    # the whole dataset is too big to open here.
    if use_random:
        if random_seed is not None:
            np.random.seed(random_seed)
        # Let's subset to fewer random trajectories:
        random_trajs = np.random.choice(np.unique(df["traj"]), num_traj, replace=False)
        traj_mask = df["traj"].apply(lambda x: x in random_trajs)
    else:
        # Let's use the first N trajectories
        first_n_trajs = np.unique(df["traj"])[:num_traj]
        traj_mask = df["traj"].apply(lambda x: x in first_n_trajs)

    df = df[traj_mask]

    df["time"] = pd.to_datetime(df["time"])

    df = df.set_index(["traj", "obs"])

    df = df.sort_index(axis=0, level=0)

    # make sure cols are called latitude and longitude
    try:
        df = df.rename(columns={"lat": "latitude"})
    except KeyError as e:
        pass
    try:
        df = df.rename(columns={"lon": "longitude"})
    except KeyError as e:
        pass

    return df

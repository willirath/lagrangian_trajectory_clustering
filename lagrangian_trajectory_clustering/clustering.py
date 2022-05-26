import editdistance

from sklearn.cluster import DBSCAN, OPTICS
from functools import partial

import pandas as pd
import numpy as np


def _edist_metric(x, y, h3_sequences, normalize=False):
    i = int(x[0])
    j = int(y[0])
    s0 = h3_sequences.iloc[i]
    s1 = h3_sequences.iloc[j]
    if not normalize:
        return editdistance.eval(s0, s1)
    else:
        return (editdistance.eval(s0, s1)) / (max(len(s0), len(s1)) + 1e-15)


def dbscan_with_edist_metric(h3_sequences, eps=0.8, normalize=True, **kwargs):
    """Run DBSCAN with edit distance.
    
    Parameters
    ----------
    h3_sequences: pandas.Series
        Series of lists of h3s.
    eps: float
        eps parameter of sklearn's DBSCAN. Defaults to 0.8.
    normalize: bool
        Normalize edit distance (value 1 if complete sequence needs replacement).
    
    All further keyword arguments are passed to sklearns DBSCAN at instantiation.

    Returns
    -------
    pandas.Series
        Cluster indices. Index is from the h3_sequences.
    
    """
    dbs = DBSCAN(
        metric=partial(_edist_metric, h3_sequences=h3_sequences, normalize=normalize),
        eps=eps,
        **kwargs,
    )
    cluster_indices = pd.Series(
        dbs.fit_predict(np.arange(len(h3_sequences)).reshape(-1, 1).astype(int)),
        index=h3_sequences.index,
        name="cluster_ids",
    )
    return cluster_indices


def optics_with_edist_metric(h3_sequences, normalize=True, **kwargs):
    """Run OPTICS with edit distance.
    
    Parameters
    ----------
    h3_sequences: pandas.Series
        Series of lists of h3s.
    normalize: bool
        Normalize edit distance (value 1 if complete sequence needs replacement).
    
    All further keyword arguments are passed to sklearns OPTICS at instantiation.

    Returns
    -------
    pandas.Series
        Cluster indices. Index is from the h3_sequences.
    
    """
    cls = OPTICS(
        metric=partial(_edist_metric, h3_sequences=h3_sequences, normalize=normalize),
        **kwargs,
    )
    cluster_indices = pd.Series(
        cls.fit_predict(np.arange(len(h3_sequences)).reshape(-1, 1).astype(int)),
        index=h3_sequences.index,
        name="cluster_ids",
    )
    return cluster_indices

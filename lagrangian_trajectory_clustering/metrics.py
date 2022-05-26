import numpy as np

from numba import jit


def lcs_numpy(x, y):
    """Calculate the longest common subsequence of x and y.

    Numpy based-implementation.

    See <https://en.wikipedia.org/wiki/Longest_common_subsequence_problem#Computing_the_length_of_the_LCS>

    Parameters
    ----------
    x: iterable
        First sequence.
    y: iterable
        First sequence.

    Even though mixed-type sequences (e.g. [1, 2, "a", "b", True]) will work here, this is not supported as
    Numba seems to have problems with it.

    Returns
    -------
    int
        Length of the longest common subsequence.

    """
    m = len(x)
    n = len(y)
    C = np.empty((m + 1, n + 1), dtype="int")
    for i in range(m + 1):
        C[i, 0] = 0
    for j in range(n + 1):
        C[0, j] = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                C[i, j] = C[i - 1, j - 1] + 1
            else:
                C[i, j] = max(C[i, j - 1], C[i - 1, j])
    return C[m, n]


def lcs_pure(x, y):
    """Calculate the longest common subsequence of x and y.

    Pure Python implementation.

    See <https://en.wikipedia.org/wiki/Longest_common_subsequence_problem#Computing_the_length_of_the_LCS>

    Parameters
    ----------
    x: iterable
        First sequence.
    y: iterable
        First sequence.

    Even though mixed-type sequences (e.g. [1, 2, "a", "b", True]) will work here, this is not supported as
    Numba seems to have problems with it.

    Returns
    -------
    int
        Length of the longest common subsequence.

    """
    m = len(x)
    n = len(y)
    C = []
    for i in range(m + 1):
        C.append(
            [
                0,
            ]
        )
    for j in range(1, n + 1):
        C[0].append(0)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                C[i].append(C[i - 1][j - 1] + 1)
            else:
                C[i].append(max(C[i][j - 1], C[i - 1][j]))
    return C[m][n]


def levenshtein_numpy(x, y):
    """Calculate the Levenshtein distance between x and y.

    Numpy based-implementation.

    See <https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm>

    Parameters
    ----------
    x: iterable
        First sequence.
    y: iterable
        First sequence.

    Even though mixed-type sequences (e.g. [1, 2, "a", "b", True]) will work here, this is not supported as
    Numba seems to have problems with it.

    Returns
    -------
    int
        Levenshtein distance.

    """
    m = len(x)
    n = len(y)
    d = np.zeros((m + 1, n + 1), dtype="int")

    for i in range(1, m + 1):
        d[i, 0] = i

    for j in range(1, n + 1):
        d[0, j] = j

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if x[i - 1] == y[j - 1]:
                cost = 0
            else:
                cost = 1

            d[i, j] = min(
                d[i - 1, j] + 1,
                d[i, j - 1] + 1,
                d[i - 1, j - 1] + cost,
            )

    return d[m, n]


lcs_numpy_numba = jit(lcs_numpy)
lcs_pure_numba = jit(lcs_pure)

levenshtein_numpy_numba = jit(levenshtein_numpy)

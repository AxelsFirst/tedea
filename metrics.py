import numpy as np

def euclidean_metric(v1, v2):
    """
    Euclidean metric between two vertices v1 and v2.

    Arguments:
    ----------
    v1: list of float
        Coordinates of first vertex.
    v2: list of float
        Coordinates of second vertex.

    Returns:
    --------
    distance: float
              Distance between parsed vertices.
    """

    return np.linalg.norm(np.array(v1) - np.array(v2))

def manhattan_metric(v1, v2):
    """
    Manhattan metric between two vertices v1 and v2.

    Arguments:
    ----------
    v1: list of float
        Coordinates of first vertex.
    v2: list of float
        Coordinates of second vertex.

    Returns:
    --------
    distance: float
              Distance between parsed vertices.
    """
    return np.linalg.norm(np.array(v1) - np.array(v2), ord=1)

def maximum_metric(v1, v2):
    """
    Chebyshev metric between two vertices v1 and v2.

    Arguments:
    ----------
    v1: list of float
        Coordinates of first vertex.
    v2: list of float
        Coordinates of second vertex.

    Returns:
    --------
    distance: float
              Distance between parsed vertices.
    """
    return np.linalg.norm(np.array(v1) - np.array(v2), ord=np.inf)
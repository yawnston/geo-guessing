from typing import List, Tuple

import numpy as np
import geopy.distance

from grid import SQUARES, Square

PREDICT_USING_TOP_K_PROBABILITIES = 8


def predict_location(probabilities: List[float]) -> Tuple[float, float]:
    sorted_indexes = np.argsort(probabilities)
    top_indexes = sorted_indexes[-PREDICT_USING_TOP_K_PROBABILITIES:]

    squares: List[Square] = []
    square_probs: List[float] = []
    for i in range(PREDICT_USING_TOP_K_PROBABILITIES):
        squares.append(SQUARES[top_indexes[i]])
        square_probs.append(probabilities[top_indexes[i]])

    square_probs_softmax = np.exp(square_probs) / sum(np.exp(square_probs))

    # Just averaging points works well enough when we are just dealing with Europe.
    # If we were doing global scale and the curvature of the Earth was
    # a factor, we would need to do more sophisticated averaging.
    # As it is, we can assume that the points are on a plane.
    lat = 0
    long = 0
    for i in range(PREDICT_USING_TOP_K_PROBABILITIES):
        lat += square_probs_softmax[i] * squares[i].center[0]
        long += square_probs_softmax[i] * squares[i].center[1]

    return (lat, long)


def distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Calculate distance between two points as kilometers.

    >>> newport_ri = (41.49008, -71.312796)
    >>> cleveland_oh = (41.499498, -81.695391)
    >>> assert (distance(newport_ri, cleveland_oh) - 866.455) < 1
    """
    return geopy.distance.distance(a, b).km


def score(distance_km: float) -> int:
    """Returns a GeoGuessr score for a given guess distance.

    The score is a value in the interval [0, 5000] where
    5000 is a near-perfect guess. The actual formula is not
    known to the public, so this function simply calculates
    an approximation of the actual formula.
    """
    return 4999.91 * (0.998036**distance_km)

"""
=========================================================
trilateration.py
3-Anchor Trilateration and 4-Anchor Multilateration
=========================================================
"""

import numpy as np


def multilaterate(anchors, distances):
    """
    Estimate the 2D tag position using multilateration.

    Parameters
    ----------
    anchors : list of tuple
        Anchor coordinates:
        [(x1, y1), (x2, y2), ...]

    distances : list
        Corresponding distances from each anchor to the tag.

    Returns
    -------
    tuple or None
        Estimated (x, y) position of the tag.
    """

    # At least 3 anchors are required for 2D localization
    if len(anchors) < 3 or len(distances) < 3:
        return None

    # Number of anchors and distances must match
    if len(anchors) != len(distances):
        return None

    # Check for invalid distance values
    if any(d is None or d <= 0 for d in distances):
        return None

    try:
        # Use the first anchor as the reference
        x1, y1 = anchors[0]
        d1 = distances[0]

        A = []
        B = []

        # Create linearized multilateration equations
        for i in range(1, len(anchors)):

            xi, yi = anchors[i]
            di = distances[i]

            A.append([
                2 * (xi - x1),
                2 * (yi - y1)
            ])

            B.append(
                d1**2
                - di**2
                - x1**2
                + xi**2
                - y1**2
                + yi**2
            )

        A = np.array(A, dtype=float)
        B = np.array(B, dtype=float)

        # Least-squares solution
        position, residuals, rank, singular_values = np.linalg.lstsq(
            A,
            B,
            rcond=None
        )

        tag_x = float(position[0])
        tag_y = float(position[1])

        return tag_x, tag_y

    except (ValueError, np.linalg.LinAlgError):
        return None


def trilaterate(anchors, distances):
    """
    Compatibility function for the existing project.

    The old project used the name 'trilaterate'.
    This function now supports both:
        - 3-anchor trilateration
        - 4-anchor multilateration
    """

    return multilaterate(anchors, distances)
from dataclasses import dataclass
import random
from typing import List, Optional, Tuple
import numpy as np
import folium


@dataclass
class Square:
    """Represents a single square on the map grid used for AI guessing."""

    left: float
    right: float
    top: float
    bottom: float
    center: Tuple[float, float]
    id: int

    def sample_points(self, num_points: int) -> List[Tuple[float, float]]:
        """Return a number of randomly sampled points which lie in this square.

        >>> for square in SQUARES:
        ...     points = square.sample_points(10000)
        ...     for point in points:
        ...         found_square = get_square_for_coords(point[0], point[1])
        ...         assert found_square == square
        """
        return [
            (
                random.uniform(self.bottom, self.top),
                random.uniform(self.left, self.right),
            )
            for _ in range(num_points)
        ]


# Coordinates were selected manually on the world map, see grid.html for
# a visualization of the grid on a map.
LEFT = 4.555298
RIGHT = 24.055298
TOP = 52.333521
BOTTOM = 45.901614

NUM_VERTICAL_SQUARES = 3
NUM_HORIZONTAL_SQUARES = 6
NUM_SQUARES = NUM_VERTICAL_SQUARES * NUM_HORIZONTAL_SQUARES

SQUARE_VERTICAL_POINTS = np.linspace(TOP, BOTTOM, num=NUM_VERTICAL_SQUARES + 1)
SQUARE_HORIZONTAL_POINTS = np.linspace(LEFT, RIGHT, num=NUM_HORIZONTAL_SQUARES + 1)


def create_square(id: int) -> Square:
    """Given a square id (sequential number from top left), create the appropriate
    square for the map grid. This means calculating the square's latitude
    and longitude from the grid's parameters.
    """
    left = SQUARE_HORIZONTAL_POINTS[id % NUM_HORIZONTAL_SQUARES]
    right = SQUARE_HORIZONTAL_POINTS[(id % NUM_HORIZONTAL_SQUARES) + 1]
    top = SQUARE_VERTICAL_POINTS[id // NUM_HORIZONTAL_SQUARES]
    bottom = SQUARE_VERTICAL_POINTS[(id // NUM_HORIZONTAL_SQUARES) + 1]

    return Square(
        id=id,
        left=left,
        right=right,
        top=top,
        bottom=bottom,
        center=((top + bottom) / 2, (left + right) / 2),
    )


# The square grid used for AI guesses
SQUARES = [create_square(id) for id in range(NUM_SQUARES)]


def get_square_for_coords(lat: float, long: float) -> Optional[Square]:
    """Given the latitude and longitude, return the corresponding square
    for that geographical location.

    >>> for square in SQUARES:
    ...    found_square = get_square_for_coords(square.center[0], square.center[1])
    ...    assert found_square == square
    """
    matching_squares = [
        square
        for square in SQUARES
        if (
            min(square.top, square.bottom) <= lat < max(square.top, square.bottom)
            and min(square.left, square.right) <= long < max(square.left, square.right)
        )
    ]

    if not matching_squares:
        return None

    # Only up to 1 square should ever match
    assert len(matching_squares) == 1
    return matching_squares[0]


def plot_grid_to_file() -> None:
    """Visualize the AI guessing grid, creating an interactive HTML map and saving it
    to a file on disk.
    """
    square_map = folium.Map(prefer_canvas=True)

    for square in SQUARES:
        # Draw the square's boundaries
        folium.PolyLine(
            [
                (square.top, square.left),
                (square.top, square.right),
                (square.bottom, square.right),
                (square.bottom, square.left),
                (square.top, square.left),
            ],
            color="red",
            weight=2.5,
            opacity=1,
        ).add_to(square_map)

        # Add a label with the square ID to the center of it
        folium.Marker(
            location=square.center,
            icon=folium.DivIcon(
                icon_size=(150, 36),
                icon_anchor=(7, 20),
                html=f'<div style="font-size: 18pt; color : black">{square.id}</div>',
            ),
        ).add_to(square_map)

    square_map.save("grid.html")


if __name__ == "__main__":
    plot_grid_to_file()

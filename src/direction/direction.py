from enum import Enum

class VerticalDirection(Enum):
    DOWN = "DOWN"
    NONE = "NONE"
    UP = "UP"

class HorizontalDirection(Enum):
    LEFT = "LEFT"
    NONE = "NONE"
    RIGHT = "RIGHT"

class Direction:
    """2D direction with 8 possible direction values and a "none" value."""

    def __init__(self, vertical_component, horizontal_component):
        """Creates a new direction object.

        Args:
            vertical_component: A direction.VerticalDirection instance.
            horizontal_component: A direction.HorizontalDirection instance.
        """

        self.__vertical_component = vertical_component
        self.__horizontal_component = horizontal_component

    def __eq__(self, other):
        """Two Directions are equal if and only if their components are equal.

        Args:
            other: A Direction instance.

        Returns:
            Boolean indicating whether this direction is equal to the other.
        """

        return (self.vertical_component == other.vertical_component and
            self.horizontal_component == other.horizontal_component)

    def __ne__(self, other):
        """Two Directions are not equal if and only if __eq__() returns False.

        Args:
            other: A Direction instance.

        Returns:
            Boolean indicating whether this direction is not equal to the other.
        """
        return not self == other

    def __hash__(self):
        """The hash of the tuple (vertical_component, horizontal_component)."""

        return hash((self.__vertical_component, self.__horizontal_component))

    def __repr__(self):
        """String of the form "<vertical_component,horizontal_component>"."""

        if self.__vertical_component == VerticalDirection.NONE:
            return f"<{self.__horizontal_component}>"
        if self.__horizontal_component == HorizontalDirection.NONE:
            return f"<{self.__vertical_component}>"

        return f"<{self.__vertical_component},{self.__horizontal_component}>"

    def __str__(self):
        """Returns the same value as __repr__()."""

        return repr(self)

    @property
    def vertical_component(self):
        """The direction.VerticalDirection instance of this Direction."""

        return self.__vertical_component

    @property
    def horizontal_component(self):
        """The direction.HorizontalDirection instance of this Direction."""

        return self.__horizontal_component

    @property
    def movement_vector(self):
        """The tuple (dx, dy), where dx and dy can have values -1, 0 or 1."""

        dx = 0
        dy = 0

        if self.__vertical_component == VerticalDirection.DOWN:
            dy = 1
        elif self.__vertical_component == VerticalDirection.UP:
            dy = -1

        if self.__horizontal_component == HorizontalDirection.LEFT:
            dx = -1
        elif self.__horizontal_component == HorizontalDirection.RIGHT:
            dx = 1

        return dx, dy

    def clip_to_four_directions(self):
        """Returns horizontal component or if it is none, vertical component."""

        if self.__horizontal_component == HorizontalDirection.LEFT:
            return LEFT
        if self.__horizontal_component == HorizontalDirection.RIGHT:
            return RIGHT
        if self.__vertical_component == VerticalDirection.DOWN:
            return DOWN
        if self.__vertical_component == VerticalDirection.UP:
            return UP

        return NONE

NONE = Direction(VerticalDirection.NONE, HorizontalDirection.NONE)
DOWN = Direction(VerticalDirection.DOWN, HorizontalDirection.NONE)
UP = Direction(VerticalDirection.UP, HorizontalDirection.NONE)
LEFT = Direction(VerticalDirection.NONE, HorizontalDirection.LEFT)
RIGHT = Direction(VerticalDirection.NONE, HorizontalDirection.RIGHT)
DOWN_LEFT = Direction(VerticalDirection.DOWN, HorizontalDirection.LEFT)
DOWN_RIGHT = Direction(VerticalDirection.DOWN, HorizontalDirection.RIGHT)
UP_LEFT = Direction(VerticalDirection.UP, HorizontalDirection.LEFT)
UP_RIGHT = Direction(VerticalDirection.UP, HorizontalDirection.RIGHT)

ALL = []
for vert_component in VerticalDirection:
    for horiz_component in HorizontalDirection:
        ALL.append(Direction(vert_component, horiz_component))

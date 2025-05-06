from enum import Enum

class HorizontalDirection(Enum):
    LEFT = "LEFT"
    NONE = "NONE"
    RIGHT = "RIGHT"

class VerticalDirection(Enum):
    DOWN = "DOWN"
    NONE = "NONE"
    UP = "UP"

class Direction:
    """2D direction with 8 possible direction values and a "none" value."""

    def __init__(self, horizontal_component, vertical_component):
        """Creates a new direction object.

        Args:
            horizontal_component: A direction.HorizontalDirection instance.
            vertical_component: A direction.VerticalDirection instance.
        """

        if (type(horizontal_component) == HorizontalDirection and
                type(vertical_component) == VerticalDirection):
            self.__horizontal_component = horizontal_component
            self.__vertical_component = vertical_component
        elif (type(horizontal_component) in (float, int) and
                type(vertical_component) in (float, int)):
            if horizontal_component > 0:
                self.__horizontal_component = HorizontalDirection.RIGHT
            elif horizontal_component < 0:
                self.__horizontal_component = HorizontalDirection.LEFT
            else:
                self.__horizontal_component = HorizontalDirection.NONE

            if vertical_component > 0:
                self.__vertical_component = VerticalDirection.DOWN
            elif vertical_component < 0:
                self.__vertical_component = VerticalDirection.UP
            else:
                self.__vertical_component = VerticalDirection.NONE
        else:
            raise TypeError("Direction.__init__() takes either a HorizontalDirection and " +
                "a VerticalDirection or two numeric values as its arguments")

    def __eq__(self, other):
        """Two Directions are equal if and only if their components are equal.

        Args:
            other: A Direction instance.

        Returns:
            Boolean indicating whether this direction is equal to the other.
        """

        return (self.horizontal_component == other.horizontal_component and
            self.vertical_component == other.vertical_component)

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

        return hash((self.__horizontal_component, self.__vertical_component))

    def __repr__(self):
        """String of the form "<horizontal_component,vertical_component>"."""

        if self.__horizontal_component == HorizontalDirection.NONE:
            return f"<{self.__vertical_component}>"
        if self.__vertical_component == VerticalDirection.NONE:
            return f"<{self.__horizontal_component}>"

        return f"<{self.__horizontal_component},{self.__vertical_component}>"

    def __str__(self):
        """Returns the same value as __repr__()."""

        return repr(self)

    @property
    def horizontal_component(self):
        """The direction.HorizontalDirection instance of this Direction."""

        return self.__horizontal_component

    @property
    def vertical_component(self):
        """The direction.VerticalDirection instance of this Direction."""

        return self.__vertical_component

    @property
    def movement_vector(self):
        """The tuple (dx, dy), where dx and dy can have values -1, 0 or 1."""

        dx = 0
        dy = 0

        if self.__horizontal_component == HorizontalDirection.LEFT:
            dx = -1
        elif self.__horizontal_component == HorizontalDirection.RIGHT:
            dx = 1

        if self.__vertical_component == VerticalDirection.DOWN:
            dy = 1
        elif self.__vertical_component == VerticalDirection.UP:
            dy = -1

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

NONE = Direction(HorizontalDirection.NONE, VerticalDirection.NONE)
DOWN = Direction(HorizontalDirection.NONE, VerticalDirection.DOWN)
UP = Direction(HorizontalDirection.NONE, VerticalDirection.UP)
LEFT = Direction(HorizontalDirection.LEFT, VerticalDirection.NONE)
RIGHT = Direction(HorizontalDirection.RIGHT, VerticalDirection.NONE)
DOWN_LEFT = Direction(HorizontalDirection.LEFT, VerticalDirection.DOWN)
DOWN_RIGHT = Direction(HorizontalDirection.RIGHT, VerticalDirection.DOWN)
UP_LEFT = Direction(HorizontalDirection.LEFT, VerticalDirection.UP)
UP_RIGHT = Direction(HorizontalDirection.RIGHT, VerticalDirection.UP)

ALL = []
for vert_component in VerticalDirection:
    for horiz_component in HorizontalDirection:
        ALL.append(Direction(horiz_component, vert_component))

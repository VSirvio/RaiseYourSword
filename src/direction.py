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
    def __init__(self, vertical_component, horizontal_component):
        self.__vertical_component = vertical_component
        self.__horizontal_component = horizontal_component

    def __eq__(self, other):
        return (self.vertical_component == other.vertical_component and
            self.horizontal_component == other.horizontal_component)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.__vertical_component, self.__horizontal_component))

    def __repr__(self):
        if self.__vertical_component == VerticalDirection.NONE:
            return f"<{self.__horizontal_component}>"
        if self.__horizontal_component == HorizontalDirection.NONE:
            return f"<{self.__vertical_component}>"

        return f"<{self.__vertical_component},{self.__horizontal_component}>"

    def __str__(self):
        return repr(self)

    @property
    def vertical_component(self):
        return self.__vertical_component

    @property
    def horizontal_component(self):
        return self.__horizontal_component

    @property
    def movement_vector(self):
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

from enum import Enum

import facing_direction

class VerticalDirection(Enum):
    DOWN = 1
    NONE = 2
    UP = 3

class HorizontalDirection(Enum):
    LEFT = 1
    NONE = 2
    RIGHT = 3

class MovementDirection:
    def __init__(self, vertical_component, horizontal_component):
        self.__vertical_component = vertical_component
        self.__horizontal_component = horizontal_component

    def __eq__(self, other):
        return (self.__vertical_component == other.__vertical_component and
            self.__horizontal_component == other.__horizontal_component)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.__vertical_component, self.__horizontal_component))

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

    @property
    def facing_direction(self):
        if self.__horizontal_component != HorizontalDirection.NONE:
            if self.__horizontal_component == HorizontalDirection.LEFT:
                return facing_direction.LEFT
            else:
                return facing_direction.RIGHT
        else:
            if self.__vertical_component == VerticalDirection.DOWN:
                return facing_direction.DOWN
            elif self.__vertical_component == VerticalDirection.UP:
                return facing_direction.UP

        return None

STAYING_STILL = MovementDirection(VerticalDirection.NONE, HorizontalDirection.NONE)

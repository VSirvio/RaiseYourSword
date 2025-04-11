from enum import Enum

class CardinalDirection(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

class FacingDirection:
    def __init__(self, direction):
        self.__direction = direction

    def __eq__(self, other):
        return self.__direction == other.__direction

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.__direction)

    def to_movement_direction(self):
        match self.__direction:
            case CardinalDirection.DOWN:
                return movement_direction.DOWN
            case CardinalDirection.UP:
                return movement_direction.UP
            case CardinalDirection.LEFT:
                return movement_direction.LEFT
            case CardinalDirection.RIGHT:
                return movement_direction.RIGHT

DOWN = FacingDirection(CardinalDirection.DOWN)
UP = FacingDirection(CardinalDirection.UP)
LEFT = FacingDirection(CardinalDirection.LEFT)
RIGHT = FacingDirection(CardinalDirection.RIGHT)

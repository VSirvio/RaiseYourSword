from direction.direction import DOWN, UP, LEFT, RIGHT

class AnimationSet:
    """Stores one type of an animation for all four directions."""

    def __init__(self, down, up, left, right):
        """Creates an animation set containing the given animations.

        Args:
            down: An Animation instance containing the downward version.
            up: An Animation instance containing the upward version.
            left: An Animation instance containing the leftward version.
            right: An Animation instance containing the rightward version.
        """

        self.__animations_by_direction = {DOWN: down, UP: up, LEFT: left, RIGHT: right}

    def __getitem__(self, direction):
        """Fetches the given direction version of the animation.

        Args:
            direction: DOWN, UP, LEFT or RIGHT from direction.direction module.

        Returns:
            The Animation instance containing the desired version.
        """

        return self.__animations_by_direction[direction]

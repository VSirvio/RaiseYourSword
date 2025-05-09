from direction.direction import DOWN, UP, LEFT, RIGHT

class AnimationSet:
    def __init__(self, down, up, left, right):
        self.__animations_by_direction = {DOWN: down, UP: up, LEFT: left, RIGHT: right}

    def __getitem__(self, direction):
        return self.__animations_by_direction[direction]

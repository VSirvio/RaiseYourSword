from direction import NONE

class CharacterDirection:
    def __init__(self, facing, moving):
        self.facing = facing
        self.__moving = moving

    @property
    def moving(self):
        return self.__moving

    @moving.setter
    def moving(self, new_movement_direction):
        self.__moving = new_movement_direction

        if new_movement_direction != NONE:
            self.facing = new_movement_direction.clip_to_four_directions()

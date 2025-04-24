import pygame

import direction

class Character(pygame.sprite.Sprite):
    def __init__(self, initial_state):
        super().__init__()

        self._facing_direction = direction.DOWN
        self._movement_direction = direction.NONE
        self._state = initial_state

    @property
    def state(self):
        return self._state.type

    @property
    def facing_direction(self):
        return self._facing_direction

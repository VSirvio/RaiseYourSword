import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, initial_state):
        super().__init__()

        self._state = initial_state

    @property
    def state(self):
        return self._state.type

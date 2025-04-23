import pygame

import direction

class Character(pygame.sprite.Sprite):
    def __init__(self, animations, initial_state):
        super().__init__()

        self._facing_direction = direction.DOWN
        self._movement_direction = direction.NONE
        self._state = initial_state

        self._animations = animations

        self._index = 0

        self.image = self._animations[self._state.type][self._facing_direction][self._index]

        self._timer = 0

        self._walk_timer = 0

    def update(self, dt):
        self._timer += dt
        self._walk_timer += dt

    def _next_index(self):
        num_of_frames = len(self._animations[self._state.type][self._facing_direction])
        return (self._index + 1) % num_of_frames

    def _reset_animation(self):
        self._index = 0
        self.image = self._animations[self._state.type][self._facing_direction][self._index]
        self._timer = 0
        self._walk_timer = 0

    @property
    def movement_direction(self):
        return self._movement_direction

    @movement_direction.setter
    def movement_direction(self, new_movement_direction):
        self._movement_direction = new_movement_direction

        if new_movement_direction != direction.NONE:
            self._facing_direction = new_movement_direction.clip_to_four_directions()

        self._reset_animation()

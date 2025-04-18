from math import atan2, pi, sqrt

import pygame

import ai.idle_state
from config import ENEMY_WALKING_SPEED, ENEMY_TO_PLAYER_MIN_DISTANCE
from direction import NONE, DOWN, UP, LEFT, RIGHT
import sprites.character

BOUNDING_BOX = pygame.Rect((20, 22), (8, 11))

WEAPON_HITBOX = {
    DOWN: pygame.Rect((0, 26), (48, 22)),
    UP: pygame.Rect((0, 0), (48, 22)),
    LEFT: pygame.Rect((0, 0), (22, 48)),
    RIGHT: pygame.Rect((26, 0), (22, 48))
}

class Enemy(sprites.character.Character):
    def __init__(self, animations):
        super().__init__(animations, ai.idle_state.IdleState())

        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 27

    def __update_state(self, state, player):
        if state is not None:
            self._state = state
            self._state.enter(enemy=self, player=player)

    def update(self, dt, **kwargs):
        player = kwargs["player"]

        super().update(dt)

        dist_x = player.rect.x - self.rect.x
        dist_y = player.rect.y - self.rect.y
        if sqrt(dist_x ** 2 + dist_y ** 2) <= ENEMY_TO_PLAYER_MIN_DISTANCE:
            self.__update_state(self._state.close_enough_to_player(), player)

        self.__update_state(self._state.update(dt=dt, enemy=self, player=player), player)

        frametime = 1000 / self._animations[self._state.type]["framerate"]
        while self._timer >= frametime:
            self._index = self._next_index()

            if self._index == 0:
                self.__update_state(self._state.animation_finished(), player)

            self._timer -= frametime

        self.image = self._animations[self._state.type][self._facing_direction][self._index]

        dx, dy = self._movement_direction.movement_vector

        time_per_px = 1000 / ENEMY_WALKING_SPEED

        # When the walking direction is diagonal, we have to multiply the time
        # it takes to walk 1 pixel (time_per_px) by sqrt(2) = ~1.1,
        # because the distance moved on the screen per pixel is that much
        # longer (compare the diagonal length of a pixel to the width/height of
        # a pixel)
        if dx != 0 and dy != 0:
            time_per_px *= sqrt(2)

        while self._walk_timer >= time_per_px:
            self._walk_timer -= time_per_px
            self.rect.x += dx
            self.rect.y += dy

    def walk(self, direction):
        if direction != NONE:
            self._facing_direction = direction.clip_to_four_directions()

        self._movement_direction = direction

        self._reset_animation()

    def attack(self, player):
        angle = atan2(self.rect.y - player.rect.y, player.rect.x - self.rect.x)
        if -3*pi/4 <= angle < -pi/4:
            self._facing_direction = DOWN
        elif -pi/4 <= angle < pi/4:
            self._facing_direction = RIGHT
        elif pi/4 <= angle < 3*pi/4:
            self._facing_direction = UP
        else:
            self._facing_direction = LEFT

        self._movement_direction = NONE

        self._reset_animation()

        current_weapon_hitbox = WEAPON_HITBOX[self._facing_direction]
        weapon_hitbox_relative_to_screen = current_weapon_hitbox.move(self.rect.x, self.rect.y)
        return weapon_hitbox_relative_to_screen.colliderect(player.bounding_box)

    @property
    def bounding_box(self):
        return BOUNDING_BOX.move(self.rect.x, self.rect.y)

    @property
    def hit_the_player(self):
        return self._state.type == "attack" and self._state.player_was_hit

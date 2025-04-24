from math import atan2, pi, sqrt

import ai.idle_state
from direction import NONE, DOWN, UP, LEFT, RIGHT
import events
import sprites.character

class Enemy(sprites.character.Character):
    def __init__(self, animations, bounding_box, weapon_hitbox, starting_position, walking_speed):
        super().__init__(animations, ai.idle_state.IdleState())

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = starting_position

        self.__bounding_box = bounding_box
        self.__weapon_hitbox = weapon_hitbox

        self.__walking_speed = walking_speed

    def __update_state(self, state, player):
        if state is not None:
            self._state = state
            self._state.enter(enemy=self, player=player)

    def update(self, dt, **kwargs):
        player = kwargs["player"]

        super().update(dt)

        self.__update_state(self._state.update(dt=dt, enemy=self, player=player), player)

        frametime = 1000 / self._animations[self._state.type]["framerate"]
        while self._timer >= frametime:
            self._index = self._next_index()

            if self._index == 0:
                new_state = self._state.handle_event(events.AnimationFinished())
                self.__update_state(new_state, player)

            self._timer -= frametime

        self.image = self._animations[self._state.type][self._facing_direction][self._index]

        dx, dy = self._movement_direction.movement_vector

        time_per_px = 1000 / self.__walking_speed

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

        self.movement_direction = NONE

        current_weapon_hitbox = self.__weapon_hitbox[self._facing_direction]
        weapon_hitbox_relative_to_screen = current_weapon_hitbox.move(self.rect.x, self.rect.y)
        if weapon_hitbox_relative_to_screen.colliderect(player.bounding_box):
            player.lose()

    @property
    def bounding_box(self):
        return self.__bounding_box.move(self.rect.x, self.rect.y)

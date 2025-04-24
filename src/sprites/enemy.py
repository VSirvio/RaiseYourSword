from math import atan2, pi

import ai.idle_state
from direction import NONE, DOWN, UP, LEFT, RIGHT
import events
import sprites.character

class Enemy(sprites.character.Character):
    def __init__(self, animations, weapon_hitbox, starting_position, physics):
        super().__init__(animations, ai.idle_state.IdleState())

        self._has_been_defeated = False

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = starting_position

        self.__weapon_hitbox = weapon_hitbox

        self.__physics = physics

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

        self.__physics.update(dt, self)

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
        return self.__physics.bounding_box.move(self.rect.x, self.rect.y)

    @property
    def has_been_defeated(self):
        return self._has_been_defeated

    def fall(self):
        self._has_been_defeated = True

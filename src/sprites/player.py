from math import sqrt

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT
from direction import NONE
import events
import sprites.character
import states.idle_state

class Player(sprites.character.Character):
    def __init__(self, animations, bounding_box, weapon_hitbox, starting_position, walking_speed):
        super().__init__(animations, states.idle_state.IdleState())

        self._has_been_defeated = False

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = starting_position

        self.__bounding_box = bounding_box

        self.__min_x = -bounding_box.x
        self.__max_x = DISPLAY_WIDTH - bounding_box.x - bounding_box.width

        self.__min_y = -bounding_box.y
        self.__max_y = DISPLAY_HEIGHT - bounding_box.y - bounding_box.height

        self.__weapon_hitbox = weapon_hitbox

        self.__walking_speed = walking_speed

        self.__direction_controlled_toward = NONE

    def __update_state(self, state, enemy):
        if state is not None:
            self._state = state
            self._state.enter(player=self, enemy=enemy)

    def update(self, dt, **kwargs):
        enemy = kwargs["enemy"]

        super().update(dt)

        frametime = 1000 / self._animations[self._state.type]["framerate"]
        while self._timer >= frametime:
            self._index = self._next_index()

            if self._index == 0:
                event = events.AnimationFinished()
                new_state = self._state.handle_event(player=self, enemy=enemy, event=event)
                self.__update_state(new_state, enemy)

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

            bbox_moved_horizontally = self.bounding_box.copy()
            bbox_moved_horizontally.x += dx
            collides_horizontally = bbox_moved_horizontally.colliderect(enemy.bounding_box)

            bbox_moved_vertically = self.bounding_box.copy()
            bbox_moved_vertically.y += dy
            collides_vertically = bbox_moved_vertically.colliderect(enemy.bounding_box)

            bbox_moved_diagonally = self.bounding_box.copy()
            bbox_moved_diagonally.x += dx
            bbox_moved_diagonally.y += dy
            collides_diagonally = bbox_moved_diagonally.colliderect(enemy.bounding_box)

            # If diagonal movement causes a collision but horizontal and vertical movement
            # don't (i.e. the corner of the bounding box collides exactly to the corner of the
            # other bounding box), then don't move the player character
            if collides_diagonally and not collides_horizontally and not collides_vertically:
                continue

            if (not collides_horizontally and (dx < 0 and self.rect.x > self.__min_x or
                    dx > 0 and self.rect.x < self.__max_x)):
                self.rect.x += dx

            if (not collides_vertically and (dy < 0 and self.rect.y > self.__min_y or
                    dy > 0 and self.rect.y < self.__max_y)):
                self.rect.y += dy

    def handle_event(self, event, enemy):
        if event.__class__ == events.MovementDirectionChanged:
            self.__direction_controlled_toward = event.new_direction

        new_state = self._state.handle_event(player=self, enemy=enemy, event=event)
        self.__update_state(new_state, enemy)

    def attack(self, enemy):
        self.movement_direction = NONE

        current_weapon_hitbox = self.__weapon_hitbox[self._facing_direction]
        weapon_hitbox_relative_to_screen = current_weapon_hitbox.move(self.rect.x, self.rect.y)
        if weapon_hitbox_relative_to_screen.colliderect(enemy.bounding_box):
            enemy.fall()

    @property
    def direction_controlled_toward(self):
        return self.__direction_controlled_toward

    @property
    def bounding_box(self):
        return self.__bounding_box.move(self.rect.x, self.rect.y)

    @property
    def has_been_defeated(self):
        return self._has_been_defeated

    def lose(self):
        self._has_been_defeated = True

        new_state = self._state.handle_event(player=self, event=events.Lose())
        self.__update_state(new_state, None)

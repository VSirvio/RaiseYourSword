from math import atan2, pi, sqrt

import pygame

import ai.idle_state
from config import ENEMY_WALKING_SPEED, ENEMY_TO_PLAYER_MIN_DISTANCE
from direction import NONE, DOWN, UP, LEFT, RIGHT

BOUNDING_BOX = pygame.Rect((20, 22), (8, 11))

WEAPON_HITBOX = {
    DOWN: pygame.Rect((0, 26), (48, 22)),
    UP: pygame.Rect((0, 0), (48, 22)),
    LEFT: pygame.Rect((0, 0), (22, 48)),
    RIGHT: pygame.Rect((26, 0), (22, 48))
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, animations):
        super().__init__()

        self.__facing_direction = DOWN
        self.__movement_direction = NONE
        self.__state = ai.idle_state.IdleState()

        self.__animations = animations

        self.__index = 0

        self.image = self.__animations[self.__state.type][self.__facing_direction][self.__index]

        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 27

        self.__timer = 0

        self.__walk_timer = 0

    def update(self, dt, **kwargs):
        player = kwargs["player"]

        dist_x = player.rect.x - self.rect.x
        dist_y = player.rect.y - self.rect.y
        if sqrt(dist_x ** 2 + dist_y ** 2) <= ENEMY_TO_PLAYER_MIN_DISTANCE:
            state = self.__state.close_enough_to_player()
            if state is not None:
                self.__state = state
                self.__state.enter(enemy=self, player=player)

        state = self.__state.update(dt=dt, enemy=self, player=player)
        if state is not None:
            self.__state = state
            self.__state.enter(enemy=self, player=player)

        self.__timer += dt
        self.__walk_timer += dt

        frametime = 1000 / self.__animations[self.__state.type]["framerate"]
        while self.__timer >= frametime:
            num_of_frames = len(self.__animations[self.__state.type][self.__facing_direction])
            self.__index = (self.__index + 1) % num_of_frames
            self.__timer -= frametime

            if self.__index == 0:
                state = self.__state.animation_finished()
                if state is not None:
                    self.__state = state
                    self.__state.enter(enemy=self, player=player)

        self.image = self.__animations[self.__state.type][self.__facing_direction][self.__index]

        dx, dy = self.__movement_direction.movement_vector

        time_per_px = 1000 / ENEMY_WALKING_SPEED

        # When the walking direction is diagonal, we have to multiply the time
        # it takes to walk 1 pixel (time_per_px) by sqrt(2) = ~1.1,
        # because the distance moved on the screen per pixel is that much
        # longer (compare the diagonal length of a pixel to the width/height of
        # a pixel)
        if dx != 0 and dy != 0:
            time_per_px *= sqrt(2)

        if self.__state.type != "attack":
            while self.__walk_timer >= time_per_px:
                self.__walk_timer -= time_per_px
                self.rect.x += dx
                self.rect.y += dy

    def walk(self, direction):
        if direction == NONE:
            self.__movement_direction = NONE
            self.__index = 0
            self.image = self.__animations[self.__state.type][self.__facing_direction][self.__index]
            self.__timer = 0
            return

        self.__facing_direction = direction.clip_to_four_directions()
        self.__index = 0
        self.image = self.__animations[self.__state.type][self.__facing_direction][self.__index]
        self.__timer = 0
        self.__walk_timer = 0

        self.__movement_direction = direction

    def attack(self, player):
        angle = atan2(self.rect.y - player.rect.y, player.rect.x - self.rect.x)
        if -3*pi/4 <= angle < -pi/4:
            self.__facing_direction = DOWN
        elif -pi/4 <= angle < pi/4:
            self.__facing_direction = RIGHT
        elif pi/4 <= angle < 3*pi/4:
            self.__facing_direction = UP
        else:
            self.__facing_direction = LEFT

        self.__movement_direction = NONE
        self.__index = 0
        self.image = self.__animations[self.__state.type][self.__facing_direction][self.__index]
        self.__timer = 0

        current_weapon_hitbox = WEAPON_HITBOX[self.__facing_direction]
        weapon_hitbox_relative_to_screen = current_weapon_hitbox.move(self.rect.x, self.rect.y)
        return weapon_hitbox_relative_to_screen.colliderect(player.bounding_box)

    @property
    def bounding_box(self):
        return BOUNDING_BOX.move(self.rect.x, self.rect.y)

    @property
    def hit_the_player(self):
        return self.__state.type == "attack" and self.__state.player_was_hit

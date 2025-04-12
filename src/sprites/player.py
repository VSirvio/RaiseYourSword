from math import sqrt

import pygame

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT
from direction import NONE, DOWN, UP, LEFT, RIGHT
from utils import centered

WALKING_SPEED = 75

BOUNDING_BOX = pygame.Rect((11, 6), (25, 36))

MIN_X = -BOUNDING_BOX.x
MAX_X = DISPLAY_WIDTH - BOUNDING_BOX.x - BOUNDING_BOX.width

MIN_Y = -BOUNDING_BOX.y
MAX_Y = DISPLAY_HEIGHT - BOUNDING_BOX.y - BOUNDING_BOX.height

WEAPON_HITBOX = {
    DOWN: pygame.Rect((0, 24), (48, 24)),
    UP: pygame.Rect((0, 0), (48, 24)),
    LEFT: pygame.Rect((0, 0), (24, 48)),
    RIGHT: pygame.Rect((24, 0), (24, 48))
}

class Player(pygame.sprite.Sprite):
    def __init__(self, animations):
        super().__init__()

        self.__has_been_defeated = False

        self.__facing_direction = DOWN
        self.__movement_direction = NONE
        self.__state = "idle"

        self.__animations = animations

        self.__index = 0

        self.image = self.__animations[self.__state][self.__facing_direction][self.__index]

        image_rect = self.image.get_rect()
        self.rect = centered(image_rect, canvas_size=(DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Set starting position a bit off the center (it looks nicer that way)
        self.rect.y -= 21

        self.__timer = 0

        self.__walk_timer = 0

    def update(self, dt, **kwargs):
        enemy = kwargs["enemy"]

        self.__timer += dt
        self.__walk_timer += dt

        frametime = 1000 / self.__animations[self.__state]["framerate"]
        while self.__timer >= frametime:
            num_of_frames = len(self.__animations[self.__state][self.__facing_direction])
            self.__index = (self.__index + 1) % num_of_frames
            self.__timer -= frametime

            if self.__state == "attack" and self.__index == 0:
                self.__state = "idle"
                self.__movement_direction = NONE
                self.__timer = 0

        self.image = self.__animations[self.__state][self.__facing_direction][self.__index]

        dx, dy = self.__movement_direction.movement_vector

        time_per_px = 1000 / WALKING_SPEED

        # When the walking direction is diagonal, we have to multiply the time
        # it takes to walk 1 pixel (time_per_px) by sqrt(2) = ~1.1,
        # because the distance moved on the screen per pixel is that much
        # longer (compare the diagonal length of a pixel to the width/height of
        # a pixel)
        if dx != 0 and dy != 0:
            time_per_px *= sqrt(2)

        if self.__state != "attack":
            while self.__walk_timer >= time_per_px:
                self.__walk_timer -= time_per_px

                bounding_box_positioned_relative_to_screen = pygame.Rect(
                    self.rect.x + BOUNDING_BOX.x,
                    self.rect.y + BOUNDING_BOX.y,
                    BOUNDING_BOX.width,
                    BOUNDING_BOX.height
                )

                bbox_moved_horizontally = bounding_box_positioned_relative_to_screen.copy()
                bbox_moved_horizontally.x += dx
                collides_horizontally = bbox_moved_horizontally.colliderect(enemy.bounding_box)

                bbox_moved_vertically = bounding_box_positioned_relative_to_screen.copy()
                bbox_moved_vertically.y += dy
                collides_vertically = bbox_moved_vertically.colliderect(enemy.bounding_box)

                bbox_moved_diagonally = bounding_box_positioned_relative_to_screen.copy()
                bbox_moved_diagonally.x += dx
                bbox_moved_diagonally.y += dy
                collides_diagonally = bbox_moved_diagonally.colliderect(enemy.bounding_box)

                # If diagonal movement causes a collision but horizontal and vertical movement
                # don't (i.e. the corner of the bounding box collides exactly to the corner of the
                # other bounding box), then don't move the player character
                if collides_diagonally and not collides_horizontally and not collides_vertically:
                    continue

                if (not collides_horizontally and (dx < 0 and self.rect.x > MIN_X or
                        dx > 0 and self.rect.x < MAX_X)):
                    self.rect.x += dx

                if (not collides_vertically and (dy < 0 and self.rect.y > MIN_Y or
                        dy > 0 and self.rect.y < MAX_Y)):
                    self.rect.y += dy

    def walk(self, direction):
        if direction == NONE:
            if self.__state != "idle":
                self.__movement_direction = NONE

                if self.__state != "attack":
                    self.__state = "idle"
                    self.__index = 0
                    self.image = self.__animations[self.__state][self.__facing_direction][self.__index]
                    self.__timer = 0
            return

        if self.__state != "attack":
            self.__state = "walk"
            if self.__facing_direction != direction.clip_to_four_directions():
                self.__facing_direction = direction.clip_to_four_directions()
                self.__index = 0
                self.image = self.__animations[self.__state][self.__facing_direction][self.__index]
                self.__timer = 0
                self.__walk_timer = 0

        self.__movement_direction = direction

    def attack(self, enemy):
        if self.__state != "attack":
            self.__state = "attack"
            self.__movement_direction = NONE
            self.__index = 0
            self.image = self.__animations[self.__state][self.__facing_direction][self.__index]
            self.__timer = 0

            weapon_hitbox_relative_to_screen = pygame.Rect(
                self.rect.x + WEAPON_HITBOX[self.__facing_direction].x,
                self.rect.y + WEAPON_HITBOX[self.__facing_direction].y,
                WEAPON_HITBOX[self.__facing_direction].width,
                WEAPON_HITBOX[self.__facing_direction].height
            )
            return weapon_hitbox_relative_to_screen.colliderect(enemy.bounding_box)

        return False

    @property
    def bounding_box(self):
        return pygame.Rect(
            self.rect.x + BOUNDING_BOX.x,
            self.rect.y + BOUNDING_BOX.y,
            BOUNDING_BOX.width,
            BOUNDING_BOX.height
        )

    @property
    def has_been_defeated(self):
        return self.__has_been_defeated

    def lose(self):
        self.__has_been_defeated = True

from math import sqrt

import pygame

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, GRAPHICS_SCALING_FACTOR
from utils import centered

WALKING_SPEED = 75

BOUNDING_BOX = pygame.Rect((11, 6), (26, 37))

MIN_X = -GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.x
MAX_X = DISPLAY_WIDTH - GRAPHICS_SCALING_FACTOR * (BOUNDING_BOX.x + BOUNDING_BOX.width)

MIN_Y = -GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.y
MAX_Y = DISPLAY_HEIGHT - GRAPHICS_SCALING_FACTOR * (BOUNDING_BOX.y + BOUNDING_BOX.height)

class Player(pygame.sprite.Sprite):
    def __init__(self, animations):
        super().__init__()

        self.__direction = "down"
        self.__dx = 0
        self.__dy = 0
        self.__state = "idle"

        self.__animations = animations

        self.__index = 0

        self.image = self.__animations[self.__state][self.__direction][self.__index]

        image_rect = self.image.get_rect()
        self.rect = centered(image_rect, canvas_size=(DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Set starting position a bit off the center (it looks nicer that way)
        self.rect.y -= 21

        self.__timer = 0

        self.__walk_timer = 0

    def update(self, dt, enemy):
        self.__timer += dt
        self.__walk_timer += dt

        frametime = 1000 / self.__animations[self.__state]["framerate"]
        while self.__timer >= frametime:
            num_of_frames = len(self.__animations[self.__state][self.__direction])
            self.__index = (self.__index + 1) % num_of_frames
            self.__timer -= frametime

            if self.__state == "attack" and self.__index == 0:
                self.__state = "idle"
                self.__dx = 0
                self.__dy = 0
                self.__timer = 0

        self.image = self.__animations[self.__state][self.__direction][self.__index]

        time_per_px = 1000 / WALKING_SPEED

        # When the walking direction is diagonal, we have to multiply the time
        # it takes to walk 1 pixel (time_per_px) by sqrt(2) = ~1.1,
        # because the distance moved on the screen per pixel is that much
        # longer (compare the diagonal length of a pixel to the width/height of
        # a pixel)
        if self.__dx != 0 and self.__dy != 0:
            time_per_px *= sqrt(2)

        if self.__state != "attack":
            while self.__walk_timer >= time_per_px:
                self.__walk_timer -= time_per_px

                bounding_box_positioned_relative_to_screen = pygame.Rect(
                    self.rect.x + GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.x,
                    self.rect.y + GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.y,
                    GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.width,
                    GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.height
                )

                bbox_moved_horizontally = bounding_box_positioned_relative_to_screen.copy()
                bbox_moved_horizontally.x += GRAPHICS_SCALING_FACTOR * self.__dx
                collides_horizontally = bbox_moved_horizontally.colliderect(enemy.bounding_box)

                bbox_moved_vertically = bounding_box_positioned_relative_to_screen.copy()
                bbox_moved_vertically.y += GRAPHICS_SCALING_FACTOR * self.__dy
                collides_vertically = bbox_moved_vertically.colliderect(enemy.bounding_box)

                bbox_moved_diagonally = bounding_box_positioned_relative_to_screen.copy()
                bbox_moved_diagonally.x += GRAPHICS_SCALING_FACTOR * self.__dx
                bbox_moved_diagonally.y += GRAPHICS_SCALING_FACTOR * self.__dy
                collides_diagonally = bbox_moved_diagonally.colliderect(enemy.bounding_box)

                # If diagonal movement causes a collision but horizontal and vertical movement
                # don't (i.e. the corner of the bounding box collides exactly to the corner of the
                # other bounding box), then don't move the player character
                if collides_diagonally and not collides_horizontally and not collides_vertically:
	                continue

                if (not collides_horizontally and (self.__dx < 0 and self.rect.x > MIN_X or
                        self.__dx > 0 and self.rect.x < MAX_X)):
                    self.rect.x += GRAPHICS_SCALING_FACTOR * self.__dx

                if (not collides_vertically and (self.__dy < 0 and self.rect.y > MIN_Y or
                        self.__dy > 0 and self.rect.y < MAX_Y)):
                    self.rect.y += GRAPHICS_SCALING_FACTOR * self.__dy

    def walk(self, vert_direction, horiz_direction):
        if vert_direction is None and horiz_direction is None:
            if self.__state != "idle":
                self.__dx = 0
                self.__dy = 0

                if self.__state != "attack":
                    self.__state = "idle"
                    self.__index = 0
                    self.image = self.__animations[self.__state][self.__direction][self.__index]
                    self.__timer = 0
            return

        if self.__state != "attack":
            self.__state = "walk"
            new_direction = horiz_direction if horiz_direction else vert_direction
            if self.__direction != new_direction:
                self.__direction = new_direction
                self.__index = 0
                self.image = self.__animations[self.__state][self.__direction][self.__index]
                self.__timer = 0
                self.__walk_timer = 0

        self.__dx = 0
        if horiz_direction == "left":
            self.__dx = -1
        elif horiz_direction == "right":
            self.__dx = 1

        self.__dy = 0
        if vert_direction == "up":
            self.__dy = -1
        elif vert_direction == "down":
            self.__dy = 1

    def attack(self):
        if self.__state != "attack":
            self.__state = "attack"
            self.__dx = 0
            self.__dy = 0
            self.__index = 0
            self.image = self.__animations[self.__state][self.__direction][self.__index]
            self.__timer = 0

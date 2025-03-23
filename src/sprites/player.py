from math import sqrt

import pygame

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, GRAPHICS_SCALING_FACTOR
from utils import centered, load_animation

WALKING_SPEED = 75

BOUNDING_BOX = pygame.Rect((10, 4), (28, 41))

MIN_X = -GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.x
MAX_X = DISPLAY_WIDTH - GRAPHICS_SCALING_FACTOR * (BOUNDING_BOX.x + BOUNDING_BOX.width)

MIN_Y = -GRAPHICS_SCALING_FACTOR * BOUNDING_BOX.y
MAX_Y = DISPLAY_HEIGHT - GRAPHICS_SCALING_FACTOR * (BOUNDING_BOX.y + BOUNDING_BOX.height)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.__direction = "down"
        self.__dx = 0
        self.__dy = 0
        self.__state = "idle"

        self.__animations = {
            "idle": {
                "framerate": 4,
                "down": load_animation("warrior", 0, 5),
                "up": load_animation("warrior", 1, 5),
                "left": load_animation("warrior", 2, 5),
                "right": load_animation("warrior", 3, 5)
            },
            "walk": {
                "framerate": 12,
                "down": load_animation("warrior", 4, 8),
                "up": load_animation("warrior", 5, 8),
                "left": load_animation("warrior", 6, 8),
                "right": load_animation("warrior", 7, 8)
            },
            "attack": {
                "framerate": 4,
                "down": load_animation("warrior", 8, 6),
                "up": load_animation("warrior", 9, 6),
                "left": load_animation("warrior", 10, 6),
                "right": load_animation("warrior", 11, 6)
            }
        }

        self.__index = 0

        self.image = self.__animations[self.__state][self.__direction][self.__index]

        image_rect = self.image.get_rect()
        self.rect = centered(image_rect, canvas_size=(DISPLAY_WIDTH, DISPLAY_HEIGHT))

        # Set starting position a bit off the center (it looks nicer that way)
        self.rect.y -= 20

        self.__timer = 0

        self.__walk_timer = 0

    def update(self, dt):
        self.__timer += dt
        self.__walk_timer += dt

        frametime = 1000 / self.__animations[self.__state]["framerate"]
        while self.__timer >= frametime:
            self.__index = (self.__index + 1) % len(self.__animations[self.__state][self.__direction])
            self.__timer -= frametime

        self.image = self.__animations[self.__state][self.__direction][self.__index]

        time_per_px = 1000 / WALKING_SPEED

        # When the walking direction is diagonal, we have to multiply the time
        # it takes to walk 1 pixel (time_per_px) by sqrt(2) = ~1.1,
        # because the distance moved on the screen per pixel is that much
        # longer (compare the diagonal length of a pixel to the width/height of
        # a pixel)
        if self.__dx != 0 and self.__dy != 0:
            time_per_px *= sqrt(2)

        while self.__walk_timer >= time_per_px:
            if ((self.__dx < 0 and self.rect.x > MIN_X) or
                    (self.__dx > 0 and self.rect.x < MAX_X)):
                self.rect.x += GRAPHICS_SCALING_FACTOR * self.__dx

            if ((self.__dy < 0 and self.rect.y > MIN_Y) or
                    (self.__dy > 0 and self.rect.y < MAX_Y)):
                self.rect.y += GRAPHICS_SCALING_FACTOR * self.__dy

            self.__walk_timer -= time_per_px

    def walk(self, vert_direction, horiz_direction):
        if vert_direction == None and horiz_direction == None:
            if self.__state != "idle":
                self.__state = "idle"
                self.__dx = 0
                self.__dy = 0
                self.__index = 0
                self.image = self.__animations[self.__state][self.__direction][self.__index]
                self.__timer = 0
            return

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

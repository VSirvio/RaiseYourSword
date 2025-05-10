import os

import pygame

from game import events
import states.game.play_state

dirname = os.path.dirname(__file__)

class CinematicTextsState:
    def __init__(self, files):
        self.__files = files

        self.__continuation_indicator_y_offset = None
        self.__continuation_indicator_timer = None
        self.__index = None
        self.__bg_sprite = None
        self.__ind_sprite = None
        self.__text_sprite = None
        self.__sprite_group = None

    def enter(self, game):
        display_width = game.config.graphics.display_width
        display_height = game.config.graphics.display_height

        self.__continuation_indicator_y_offset = 0
        self.__continuation_indicator_timer = 0

        self.__index = 0

        self.__bg_sprite = pygame.sprite.Sprite()
        self.__bg_sprite.image = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
        self.__bg_sprite.image.fill(pygame.Color(0, 0, 0, 190))
        self.__bg_sprite.rect = self.__bg_sprite.image.get_rect()

        self.__ind_sprite = pygame.sprite.Sprite()
        self.__ind_sprite.image = pygame.image.load(
            os.path.join(dirname, "..", "..", "assets", "white_down-pointing_triangle.png")
        )
        self.__ind_sprite.rect = self.__ind_sprite.image.get_rect()

        self.__text_sprite = pygame.sprite.Sprite()
        self.__load_image(
            self.__text_sprite,
            self.__ind_sprite,
            self.__files[self.__index],
            (game.config.graphics.display_width, game.config.graphics.display_height)
        )

        self.__sprite_group = pygame.sprite.LayeredUpdates(
            self.__bg_sprite,
            self.__text_sprite,
            self.__ind_sprite
        )
        self.__sprite_group.change_layer(self.__bg_sprite, 1)
        self.__sprite_group.change_layer(self.__text_sprite, 2)
        self.__sprite_group.change_layer(self.__ind_sprite, 3)

    def __load_image(self, text_sprite, ind_sprite, file, display_size):
        display_width, display_height = display_size

        text_sprite.image = pygame.image.load(file)
        text_sprite.rect = text_sprite.image.get_rect()
        text_sprite.rect.x = (display_width - text_sprite.rect.width) // 2
        text_sprite.rect.y = (display_height - text_sprite.rect.height) // 2

        ind_sprite.rect.x = (display_width + text_sprite.rect.width) // 2 + 9
        ind_sprite.rect.y = ((display_height + text_sprite.rect.height) // 2 - 2 +
            self.__continuation_indicator_y_offset)

    def update(self, *args):
        dt = args[0]

        self.__continuation_indicator_timer += dt
        while self.__continuation_indicator_timer >= 450:
            self.__continuation_indicator_timer -= 450
            if self.__continuation_indicator_y_offset == 0:
                self.__continuation_indicator_y_offset = 1
                self.__ind_sprite.rect.y += 1
            else:
                self.__continuation_indicator_y_offset = 0
                self.__ind_sprite.rect.y -= 1

    def handle_event(self, *args):
        event = args[0]
        game = args[1]

        match event.__class__:
            case events.Accept:
                if self.__index + 1 < len(self.__files):
                    self.__index += 1
                    self.__load_image(
                        self.__text_sprite,
                        self.__ind_sprite,
                        self.__files[self.__index],
                        (game.config.graphics.display_width, game.config.graphics.display_height)
                    )
                else:
                    return states.game.play_state.PlayState()

        return None

    @property
    def sprite_group(self):
        return self.__sprite_group

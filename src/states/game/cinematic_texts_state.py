import os

import pygame

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT
import events
import states.game.play_state

dirname = os.path.dirname(__file__)

class CinematicTextsState:
    def __init__(self, files):
        self.__continuation_indicator_position = None
        self.__continuation_indicator_y_offset = 0
        self.__continuation_indicator_timer = 0
        self.__continuation_indicator_surface = pygame.image.load(
            os.path.join(dirname, "..", "..", "assets", "white_down-pointing_triangle.png")
        )

        self.__files = files
        self.__index = 0
        self.__surface = self.__load_image(self.__files[self.__index])

    def __load_image(self, file):
        surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)

        transparent_black = pygame.Color(0, 0, 0, 190)
        surface.fill(transparent_black)

        text = pygame.image.load(file)
        center_pos = (
            (DISPLAY_WIDTH - text.get_width()) // 2,
            (DISPLAY_HEIGHT - text.get_height()) // 2
        )
        surface.blit(text, center_pos)

        self.__continuation_indicator_position = (
            (DISPLAY_WIDTH + text.get_width()) // 2 + 9,
            (DISPLAY_HEIGHT + text.get_height()) // 2 - 2
        )

        return surface

    def draw(self, surface):
        surface.blit(self.__surface, (0, 0))

        surface.blit(
            self.__continuation_indicator_surface,
            (
                self.__continuation_indicator_position[0],
                self.__continuation_indicator_position[1] + self.__continuation_indicator_y_offset
            )
        )

    def update(self, *args):
        dt = args[0]

        self.__continuation_indicator_timer += dt
        while self.__continuation_indicator_timer >= 450:
            self.__continuation_indicator_timer -= 450
            if self.__continuation_indicator_y_offset == 0:
                self.__continuation_indicator_y_offset = 1
            else:
                self.__continuation_indicator_y_offset = 0

    def handle_event(self, *args):
        event = args[0]

        match event.__class__:
            case events.Accept:
                if self.__index + 1 < len(self.__files):
                    self.__index += 1
                    self.__surface = self.__load_image(self.__files[self.__index])
                else:
                    return states.game.play_state.PlayState()

        return None

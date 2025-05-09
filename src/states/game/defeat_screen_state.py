import os

import pygame

from game.config import DISPLAY_WIDTH, DISPLAY_HEIGHT

dirname = os.path.dirname(__file__)

class DefeatScreenState:
    def __init__(self):
        self.__surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)

        transparent_black = pygame.Color(0, 0, 0, 190)
        self.__surface.fill(transparent_black)

        defeat_text = pygame.image.load(
            os.path.join(dirname, "..", "..", "assets", "defeat_message.png")
        )
        self.__surface.blit(defeat_text, (38, 90))

        instructions = pygame.image.load(
            os.path.join(dirname, "..", "..", "assets", "defeat_instructions.png")
        )
        self.__surface.blit(instructions, (55, 170))

    def draw(self, surface):
        surface.blit(self.__surface, (0, 0))

    def update(self, *args):
        pass

    def handle_event(self, *args):
        pass

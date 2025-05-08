import os

import pygame

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT

dirname = os.path.dirname(__file__)

class VictoryScreenState:
    def __init__(self):
        self.__surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)

        transparent_black = pygame.Color(0, 0, 0, 190)
        self.__surface.fill(transparent_black)

        victory_text = pygame.image.load(
            os.path.join(dirname, "..", "..", "assets", "victory_message.png")
        )
        self.__surface.blit(victory_text, (36, 100))

        instructions = pygame.image.load(
            os.path.join(dirname, "..", "..", "assets", "victory_instructions.png")
        )
        self.__surface.blit(instructions, (36, 167))

    def draw(self, surface):
        surface.blit(self.__surface, (0, 0))

    def update(self, *args):
        pass

    def handle_event(self, *args):
        pass

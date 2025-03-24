import pygame

class Renderer:
    def __init__(self, display, game):
        self.__display = display
        self.__game = game

    def render(self):
        self.__game.draw(self.__display)

        pygame.display.update()

import os

import pygame

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT
from game import Game
from game_loop import GameLoop

dirname = os.path.dirname(__file__)

def main():
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    pygame.display.set_caption("Raise Your Sword")

    win_icon = pygame.image.load(os.path.join(dirname, "assets", "icon_skull.png"))
    pygame.display.set_icon(win_icon)

    game = Game()

    game_loop = GameLoop(game, display)

    pygame.init()
    game_loop.start()

if __name__ == "__main__":
    main()

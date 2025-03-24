import os

import pygame

from clock import Clock
from config import DISPLAY_WIDTH, DISPLAY_HEIGHT
from event_queue import EventQueue
from game import Game
from game_loop import GameLoop
from renderer import Renderer

dirname = os.path.dirname(__file__)

def main():
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    pygame.display.set_caption("Raise Your Sword")

    win_icon = pygame.image.load(os.path.join(dirname, "assets", "icon_skull.png"))
    pygame.display.set_icon(win_icon)

    game = Game()
    renderer = Renderer(display, game)
    event_queue = EventQueue()
    clock = Clock()
    game_loop = GameLoop(game, renderer, event_queue, clock)

    pygame.init()
    game_loop.start()

if __name__ == "__main__":
    main()

import os

import pygame

from clock import Clock
from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, GRAPHICS_SCALING_FACTOR
from event_queue import EventQueue
from game import Game
from game_loop import GameLoop
from renderer import Renderer

dirname = os.path.dirname(__file__)

def main():
    pygame.init()
    display = pygame.display.set_mode((
        DISPLAY_WIDTH * GRAPHICS_SCALING_FACTOR,
        DISPLAY_HEIGHT * GRAPHICS_SCALING_FACTOR
    ))

    pygame.display.set_caption("Raise Your Sword")

    win_icon = pygame.image.load(os.path.join(dirname, "assets", "icon_skull.png"))
    pygame.display.set_icon(win_icon)

    start_new_game = True
    is_first_game = True

    while start_new_game:
        game = Game(skip_intro=not is_first_game)
        renderer = Renderer(display, game, GRAPHICS_SCALING_FACTOR)
        event_queue = EventQueue()
        clock = Clock()
        game_loop = GameLoop(game, renderer, event_queue, clock)

        start_new_game = game_loop.start()

        is_first_game = False

if __name__ == "__main__":
    main()

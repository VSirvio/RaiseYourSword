import os

import pygame

from config import generate_configuration
from game.game import Game
from game.game_loop import GameLoop
from services.clock import Clock
from services.event_queue import EventQueue
from services.renderer import Renderer

dirname = os.path.dirname(__file__)

def main():
    config = generate_configuration()

    pygame.init()
    display = pygame.display.set_mode((
        config.graphics.display_width * config.graphics.scaling_factor,
        config.graphics.display_height * config.graphics.scaling_factor
    ))

    pygame.display.set_caption("Raise Your Sword")

    win_icon = pygame.image.load(os.path.join(dirname, "assets", "icon_skull.png"))
    pygame.display.set_icon(win_icon)

    start_new_game = True
    is_first_game = True

    while start_new_game:
        game = Game(config, skip_intro=not is_first_game)
        renderer = Renderer(display, game, config.graphics.scaling_factor)
        event_queue = EventQueue()
        clock = Clock()
        game_loop = GameLoop(game, renderer, event_queue, clock)

        start_new_game = game_loop.start()

        is_first_game = False

if __name__ == "__main__":
    main()

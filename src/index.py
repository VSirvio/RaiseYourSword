import os

import pygame

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT
from game import Game

dirname = os.path.dirname(__file__)

def main():
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    pygame.display.set_caption("Raise Your Sword")

    win_icon = pygame.image.load(os.path.join(dirname, "assets", "icon_skull.png"))
    pygame.display.set_icon(win_icon)

    clock = pygame.time.Clock()

    game = Game()

    pygame.init()

    running = True
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    game.walk("down")
                elif event.key == pygame.K_UP:
                    game.walk("up")
                elif event.key == pygame.K_LEFT:
                    game.walk("left")
                elif event.key == pygame.K_RIGHT:
                    game.walk("right")
            elif event.type == pygame.KEYUP:
                game.stop_player()
            elif event.type == pygame.QUIT:
                running = False

        game.update(dt)

        game.draw(display)

        pygame.display.update()

        dt = clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

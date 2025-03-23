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
    key_pressed = {"down": False, "up": False, "left": False, "right": False}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    key_pressed["down"] = True
                elif event.key in (pygame.K_UP, pygame.K_w):
                    key_pressed["up"] = True
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    key_pressed["left"] = True
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    key_pressed["right"] = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    key_pressed["down"] = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    key_pressed["up"] = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    key_pressed["left"] = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    key_pressed["right"] = False
            elif event.type == pygame.QUIT:
                running = False

        vert_direction = None
        if key_pressed["up"]:
            if key_pressed["down"]:
                vert_direction = None
            else:
                vert_direction = "up"
        elif key_pressed["down"]:
            vert_direction = "down"

        horiz_direction = None
        if key_pressed["left"]:
            if key_pressed["right"]:
                horiz_direction = None
            else:
                horiz_direction = "left"
        elif key_pressed["right"]:
            horiz_direction = "right"

        game.walk(vert_direction, horiz_direction)

        game.update(dt)

        game.draw(display)

        pygame.display.update()

        dt = clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

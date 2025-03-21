import os

import pygame

from config import GRAPHICS_SCALING_FACTOR
from utils import fill_with_tile

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

dirname = os.path.dirname(__file__)

def main():
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    pygame.display.set_caption("Raise Your Sword")

    win_icon = pygame.image.load(os.path.join(dirname, "assets", "icon_skull.png"))
    pygame.display.set_icon(win_icon)

    bg_tile = pygame.image.load(os.path.join(dirname, "assets", "background_tile_grass.png"))
    bg_tile = pygame.transform.scale_by(bg_tile, GRAPHICS_SCALING_FACTOR)

    bg = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    fill_with_tile(bg, bg_tile)

    pygame.init()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.blit(bg, (0, 0))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

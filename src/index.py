import math
import os

import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

GRAPHICS_SCALING_FACTOR = 3

dirname = os.path.dirname(__file__)

def main():
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    pygame.display.set_caption("Raise Your Sword")

    bg_tile = pygame.image.load(os.path.join(dirname, "assets", "background_tile_grass.png"))
    bg_tile = pygame.transform.scale_by(bg_tile, GRAPHICS_SCALING_FACTOR)

    bg = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    for x in range(math.ceil(DISPLAY_WIDTH / bg_tile.get_width())):
        for y in range(math.ceil(DISPLAY_HEIGHT / bg_tile.get_height())):
            bg.blit(bg_tile, (x * bg_tile.get_width(), y * bg_tile.get_height()))

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

import os

import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

dirname = os.path.dirname(__file__)

def main():
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    pygame.display.set_caption("Raise Your Sword")

    bg = pygame.image.load(os.path.join(dirname, "assets", "background_tile_grass.png")).convert()

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

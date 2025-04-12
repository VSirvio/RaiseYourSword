import pygame

class Renderer:
    def __init__(self, display, game, graphics_scaling_factor):
        self.__display = display
        self.__game = game
        self.__graphics_scaling_factor = graphics_scaling_factor

        self.__intermediate_surface = pygame.Surface((
            display.get_width() // graphics_scaling_factor,
            display.get_height() // graphics_scaling_factor
        ))

    def render(self):
        self.__game.draw(self.__intermediate_surface)

        scaled_surface = pygame.transform.scale_by(
            self.__intermediate_surface,
            self.__graphics_scaling_factor
        )
        self.__display.blit(scaled_surface, (0, 0))

        pygame.display.update()

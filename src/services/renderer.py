import pygame

class Renderer:
    """Provides the game means to draw its graphics on the screen."""

    def __init__(self, display, game, graphics_scaling_factor):
        """Creates a new renderer with the given parameters.

        Args:
            display: Display surface returned by pygame.display.set_mode().
            game: Game object whose graphics are to be rendered.
            graphics_scaling_factor: Size of one game pixel in screen pixels.
        """

        self.__display = display
        self.__game = game
        self.__graphics_scaling_factor = graphics_scaling_factor

        self.__intermediate_surface = pygame.Surface((
            display.get_width() // graphics_scaling_factor,
            display.get_height() // graphics_scaling_factor
        ))

    def render(self):
        """Renders game graphics scaled by the factor on the display surface."""

        self.__game.draw(self.__intermediate_surface)

        scaled_surface = pygame.transform.scale_by(
            self.__intermediate_surface,
            self.__graphics_scaling_factor
        )
        self.__display.blit(scaled_surface, (0, 0))

        pygame.display.update()

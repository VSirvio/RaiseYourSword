class GraphicsConfig:
    """Stores the graphics configuration for the game."""

    def __init__(self, display_size, scaling_factor):
        """Creates a graphics configuration with the given parameters.

        Args:
            display_size: A tuple containing display width and height in pixels.
            scaling_factor: The number of screen pixels a game pixel is wide.
        """

        self.__display_width, self.__display_height = display_size
        self.__scaling_factor = scaling_factor

    @property
    def display_width(self):
        """An integer value indicating the display width in pixels."""

        return self.__display_width

    @property
    def display_height(self):
        """An integer value indicating the display height in pixels."""

        return self.__display_height

    @property
    def scaling_factor(self):
        """The number of screen pixels that a game pixel is wide (and high)."""

        return self.__scaling_factor

class GameConfig:
    """Stores all the configuration for the game."""

    def __init__(self, graphics_config, ai_config, spawning_config):
        """Creates a game configuration with the given parameters.

        Args:
            graphics_config: A GraphicsConfig instance.
            ai_config: An AiConfig instance.
            spawning_config: A SpawningConfig instance.
        """

        self.__graphics_config = graphics_config
        self.__ai_config = ai_config
        self.__spawning_config = spawning_config

    @property
    def graphics(self):
        """The GraphicsConfig of this game configuration."""

        return self.__graphics_config

    @property
    def ai(self):
        """The AiConfig of this game configuration."""

        return self.__ai_config

    @property
    def spawning(self):
        """The SpawningConfig of this game configuration."""

        return self.__spawning_config

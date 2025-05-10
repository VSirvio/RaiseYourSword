class GameConfig:
    def __init__(self, graphics_config, ai_config, spawning_config):
        self.__graphics_config = graphics_config
        self.__ai_config = ai_config
        self.__spawning_config = spawning_config

    @property
    def graphics(self):
        return self.__graphics_config

    @property
    def ai(self):
        return self.__ai_config

    @property
    def spawning(self):
        return self.__spawning_config

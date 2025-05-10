class GraphicsConfig:
    def __init__(self, display_size, scaling_factor):
        self.__display_width, self.__display_height = display_size
        self.__scaling_factor = scaling_factor

    @property
    def display_width(self):
        return self.__display_width

    @property
    def display_height(self):
        return self.__display_height

    @property
    def scaling_factor(self):
        return self.__scaling_factor

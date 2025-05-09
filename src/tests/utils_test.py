import unittest

from game.graphics_utils import fill_with_tile


class StubSurface:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__blit_method_calls = []

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def blit(self, source, dest):
        self.__blit_method_calls.append((source, dest))

    @property
    def blit_method_calls(self):
        return self.__blit_method_calls


class TestUtils(unittest.TestCase):
    def test_fill_with_tile_function_fills_the_canvas_properly(self):
        canvas = StubSurface(100, 75)
        tile = StubSurface(32, 31)

        fill_with_tile(canvas, tile)

        self.assertCountEqual(
            canvas.blit_method_calls,
            [(tile, dest) for dest in [
                (0, 0), (32, 0), (64, 0), (96, 0),
                (0, 31), (32, 31), (64, 31), (96, 31),
                (0, 62), (32, 62), (64, 62), (96, 62)
            ]]
        )

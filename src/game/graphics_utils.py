import math

def fill_with_tile(canvas, tile):
    """Fills a pygame surface by repeating a smaller pygame surface.

    Args:
        canvas: A pygame surface to fill.
        tile: A smaller pygame surface that the other surface is filled with.
    """

    for x in range(math.ceil(canvas.get_width() / tile.get_width())):
        for y in range(math.ceil(canvas.get_height() / tile.get_height())):
            canvas.blit(tile, (x * tile.get_width(), y * tile.get_height()))

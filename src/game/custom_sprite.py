import pygame

class CustomSprite(pygame.sprite.Sprite):
    """Pygame Sprite sub class whose update() calls given Character's update."""

    def __init__(self, owner):
        """Creates a custom sprite for the given Character instance.

        Args:
            owner: A Character instance that owns this custom sprite.
        """

        super().__init__()
        self.__owner = owner

    def update(self, dt, **kwargs):
        """The update method of the pygame Sprite class.

        Args:
            dt: The time elapsed from the last iteration of the game loop.
        """

        self.__owner.update(dt, **kwargs)

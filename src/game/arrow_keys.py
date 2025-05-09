import pygame

from direction.direction import Direction, HorizontalDirection, VerticalDirection

class ArrowKeys:
    """Decides which direction to move based on the arrow/WASD keys pressed."""

    def __init__(self):
        self.__down_key_pressed = False
        self.__up_key_pressed = False
        self.__left_key_pressed = False
        self.__right_key_pressed = False

    def handle(self, event):
        """Update the movement direction based on a new pygame input event.

        Args:
            event: A pygame.event.Event instance.

        Returns:
            A boolean value indicating whether the movement direction changed.
        """

        if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
            return False

        match event.key:
            case pygame.K_DOWN | pygame.K_s:
                self.__down_key_pressed = event.type == pygame.KEYDOWN
            case pygame.K_UP | pygame.K_w:
                self.__up_key_pressed = event.type == pygame.KEYDOWN
            case pygame.K_LEFT | pygame.K_a:
                self.__left_key_pressed = event.type == pygame.KEYDOWN
            case pygame.K_RIGHT | pygame.K_d:
                self.__right_key_pressed = event.type == pygame.KEYDOWN
            case _:
                return False

        return True

    def release_all(self):
        """Reset the state as if no arrow or WASD key was pressed."""

        self.__down_key_pressed = False
        self.__up_key_pressed = False
        self.__left_key_pressed = False
        self.__right_key_pressed = False

    @property
    def current_direction(self):
        """A Direction object giving the direction according to pressed keys."""

        vertical_direction = VerticalDirection.NONE
        if self.__up_key_pressed and not self.__down_key_pressed:
            vertical_direction = VerticalDirection.UP
        elif self.__down_key_pressed and not self.__up_key_pressed:
            vertical_direction = VerticalDirection.DOWN

        horizontal_direction = HorizontalDirection.NONE
        if self.__left_key_pressed and not self.__right_key_pressed:
            horizontal_direction = HorizontalDirection.LEFT
        elif self.__right_key_pressed and not self.__left_key_pressed:
            horizontal_direction = HorizontalDirection.RIGHT

        return Direction(vertical_direction, horizontal_direction)

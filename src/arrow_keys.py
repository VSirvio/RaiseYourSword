import pygame

from direction import Direction, HorizontalDirection, VerticalDirection

class ArrowKeys:
    def __init__(self):
        self.__down_key_pressed = False
        self.__up_key_pressed = False
        self.__left_key_pressed = False
        self.__right_key_pressed = False

    def handle(self, event):
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
        self.__down_key_pressed = False
        self.__up_key_pressed = False
        self.__left_key_pressed = False
        self.__right_key_pressed = False

    @property
    def current_direction(self):
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

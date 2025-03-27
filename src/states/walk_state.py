import pygame

from utils import get_direction

class WalkState:
    def __init__(self, vert_direction, horiz_direction):
        self.__vert_direction = vert_direction
        self.__horiz_direction = horiz_direction

    def enter(self, sprite):
        sprite.walk(self.__vert_direction, self.__horiz_direction)

    def handle_input(self, event, key_pressed):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
            return AttackState()

        vert_direction, horiz_direction = get_direction(key_pressed)
        if vert_direction != self.__vert_direction or horiz_direction != self.__horiz_direction:
            if vert_direction is None and horiz_direction is None:
                return IdleState()
            return WalkState(vert_direction, horiz_direction)

        return None

    def animation_finished(self):
        return None

    def __str__(self):
        return "walk"

from states.attack_state import AttackState
from states.idle_state import IdleState

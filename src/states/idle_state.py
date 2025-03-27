import pygame

from utils import get_direction

class IdleState:
    def enter(self, sprite):
        sprite.walk(None, None)

    def handle_input(self, event, key_pressed):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
            return AttackState()

        vert_direction, horiz_direction = get_direction(key_pressed)
        if vert_direction is not None or horiz_direction is not None:
            return WalkState(vert_direction, horiz_direction)

        return None

    def animation_finished(self):
        return None

    def __str__(self):
        return "idle"

from states.attack_state import AttackState
from states.walk_state import WalkState

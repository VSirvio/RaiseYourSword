import pygame

import direction
import states.attack_state   # pylint: disable=cyclic-import
import states.idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class WalkState:
    def __init__(self, walk_direction):
        self.__direction = walk_direction

    @property
    def type(self):
        return "walk"

    def enter(self, **kwargs):
        kwargs["player"].movement_direction = self.__direction

    def handle_input(self, **kwargs):
        event = kwargs["event"]
        direction_pressed = kwargs["direction_pressed"]

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
            return states.attack_state.AttackState()

        if direction_pressed != self.__direction:
            if direction_pressed == direction.NONE:
                return states.idle_state.IdleState()
            return WalkState(direction_pressed)

        return None

    def animation_finished(self, player):
        return None

    def has_been_defeated(self):
        return states.idle_state.IdleState()

from math import atan2, pi

import ai.idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).
from direction import NONE, DOWN, UP, RIGHT, LEFT
import events
import state

class AttackState(state.State):
    def enter(self, **kwargs):
        owner = kwargs["owner"]
        opponent = kwargs["opponent"]

        angle = atan2(owner.rect.y - opponent.rect.y, opponent.rect.x - owner.rect.x)
        if -3*pi/4 <= angle < -pi/4:
            owner.direction.moving = DOWN
        elif -pi/4 <= angle < pi/4:
            owner.direction.moving = RIGHT
        elif pi/4 <= angle < 3*pi/4:
            owner.direction.moving = UP
        else:
            owner.direction.moving = LEFT

        owner.direction.moving = NONE

        if owner.does_attack_hit(opponent):
            opponent.defeat()

    def handle_event(self, **kwargs):
        event = kwargs["event"]

        match event.__class__:
            case events.AnimationFinished:
                return ai.idle_state.IdleState()

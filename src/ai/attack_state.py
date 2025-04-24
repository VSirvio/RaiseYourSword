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
        enemy = kwargs["enemy"]
        player = kwargs["player"]

        angle = atan2(enemy.rect.y - player.rect.y, player.rect.x - enemy.rect.x)
        if -3*pi/4 <= angle < -pi/4:
            enemy.movement_direction = DOWN
        elif -pi/4 <= angle < pi/4:
            enemy.movement_direction = RIGHT
        elif pi/4 <= angle < 3*pi/4:
            enemy.movement_direction = UP
        else:
            enemy.movement_direction = LEFT

        enemy.movement_direction = NONE

        if enemy.does_attack_hit(player):
            player.lose()

    def update(self, **kwargs):
        return None

    def handle_event(self, event):
        match event.__class__:
            case events.AnimationFinished:
                return ai.idle_state.IdleState()

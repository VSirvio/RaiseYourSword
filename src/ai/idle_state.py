from math import sqrt
from random import randrange

from config import ENEMY_TO_PLAYER_MIN_DISTANCE, ENEMY_AI_IDLE_TIME_MIN, ENEMY_AI_IDLE_TIME_MAX
import direction
import ai.attack_state   # pylint: disable=cyclic-import
import ai.walk_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).
import state

class IdleState(state.State):
    def __init__(self):
        self.__duration = randrange(ENEMY_AI_IDLE_TIME_MIN, ENEMY_AI_IDLE_TIME_MAX)
        self.__timer = 0

    def enter(self, **kwargs):
        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

    def update(self, **kwargs):
        owner = kwargs["owner"]
        opponent = kwargs["opponent"]

        if opponent.has_been_defeated:
            return None

        self.__timer += kwargs["dt"]

        if self.__timer >= self.__duration:
            dist_x = opponent.rect.x - owner.rect.x
            dist_y = opponent.rect.y - owner.rect.y
            if sqrt(dist_x ** 2 + dist_y ** 2) <= ENEMY_TO_PLAYER_MIN_DISTANCE:
                return ai.attack_state.AttackState()
            return ai.walk_state.WalkState()

        return None

    def handle_event(self, **kwargs):
        return None

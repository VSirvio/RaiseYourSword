from math import atan2, pi, sqrt
from random import randrange

from config import ENEMY_TO_PLAYER_MIN_DISTANCE, ENEMY_AI_WALK_TIME_MIN, ENEMY_AI_WALK_TIME_MAX
import direction
import ai.idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).
import state

class WalkState(state.State):
    def __init__(self):
        self.__duration = randrange(ENEMY_AI_WALK_TIME_MIN, ENEMY_AI_WALK_TIME_MAX)
        self.__timer = 0

    def enter(self, **kwargs):
        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]

        angle = atan2(owner.y - opponent.y, opponent.x - owner.x)
        if -7*pi/8 <= angle < -5*pi/8:
            owner.direction.moving = direction.DOWN_LEFT
        elif -5*pi/8 <= angle < -3*pi/8:
            owner.direction.moving = direction.DOWN
        elif -3*pi/8 <= angle < -pi/8:
            owner.direction.moving = direction.DOWN_RIGHT
        elif -pi/8 <= angle < pi/8:
            owner.direction.moving = direction.RIGHT
        elif pi/8 <= angle < 3*pi/8:
            owner.direction.moving = direction.UP_RIGHT
        elif 3*pi/8 <= angle < 5*pi/8:
            owner.direction.moving = direction.UP
        elif 5*pi/8 <= angle < 7*pi/8:
            owner.direction.moving = direction.UP_LEFT
        else:
            owner.direction.moving = direction.LEFT

    def update(self, **kwargs):
        dt = kwargs["dt"]
        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]

        self.__timer += dt

        if self.__timer >= self.__duration:
            return ai.idle_state.IdleState()

        dist_x = opponent.x - owner.x
        dist_y = opponent.y - owner.y
        if sqrt(dist_x ** 2 + dist_y ** 2) <= ENEMY_TO_PLAYER_MIN_DISTANCE:
            return ai.idle_state.IdleState()

        return None

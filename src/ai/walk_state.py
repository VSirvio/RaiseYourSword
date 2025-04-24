from math import atan2, pi
from random import randrange

from config import ENEMY_AI_WALK_TIME_MIN, ENEMY_AI_WALK_TIME_MAX
import direction
import ai.idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).
import state

class WalkState(state.State):
    def __init__(self, enemy, player):
        self.__duration = randrange(ENEMY_AI_WALK_TIME_MIN, ENEMY_AI_WALK_TIME_MAX)
        self.__timer = 0

        angle = atan2(enemy.rect.y - player.rect.y, player.rect.x - enemy.rect.x)
        if -7*pi/8 <= angle < -5*pi/8:
            self.__direction = direction.DOWN_LEFT
        elif -5*pi/8 <= angle < -3*pi/8:
            self.__direction = direction.DOWN
        elif -3*pi/8 <= angle < -pi/8:
            self.__direction = direction.DOWN_RIGHT
        elif -pi/8 <= angle < pi/8:
            self.__direction = direction.RIGHT
        elif pi/8 <= angle < 3*pi/8:
            self.__direction = direction.UP_RIGHT
        elif 3*pi/8 <= angle < 5*pi/8:
            self.__direction = direction.UP
        elif 5*pi/8 <= angle < 7*pi/8:
            self.__direction = direction.UP_LEFT
        else:
            self.__direction = direction.LEFT

    def enter(self, **kwargs):
        kwargs["enemy"].movement_direction = self.__direction

    def update(self, **kwargs):
        self.__timer += kwargs["dt"]

        if self.__timer >= self.__duration:
            return ai.idle_state.IdleState()

        return None

    def animation_finished(self):
        return None

    def close_enough_to_player(self):
        return ai.idle_state.IdleState()

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

class IdleState:
    def __init__(self, game_finished=False):
        self.__duration = randrange(ENEMY_AI_IDLE_TIME_MIN, ENEMY_AI_IDLE_TIME_MAX)
        self.__timer = 0
        self.__game_finished = game_finished

    @property
    def type(self):
        return "idle"

    def enter(self, **kwargs):
        kwargs["enemy"].walk(direction.NONE)

    def update(self, **kwargs):
        enemy = kwargs["enemy"]
        player = kwargs["player"]

        if self.__game_finished:
            return None

        self.__timer += kwargs["dt"]

        if self.__timer >= self.__duration:
            dist_x = player.rect.x - enemy.rect.x
            dist_y = player.rect.y - enemy.rect.y
            if sqrt(dist_x ** 2 + dist_y ** 2) <= ENEMY_TO_PLAYER_MIN_DISTANCE:
                return ai.attack_state.AttackState()
            return ai.walk_state.WalkState(enemy=enemy, player=player)

        return None

    def animation_finished(self):
        return None

    def close_enough_to_player(self):
        return None

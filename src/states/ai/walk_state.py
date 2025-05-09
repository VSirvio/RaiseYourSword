from math import atan2, pi, sqrt
from random import randrange

from direction import direction
from game import events
from game.config import (
    ENEMY_AI_WALK_TIME_MAX,
    ENEMY_AI_WALK_TIME_MIN,
    ENEMY_ATTACK_INITIATION_DISTANCE
)
import states.state
import states.ai.idle_state   # pylint: disable=cyclic-import
import states.character.dying_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).

class WalkState(states.state.State):
    def __init__(self):
        self.__duration = randrange(ENEMY_AI_WALK_TIME_MIN, ENEMY_AI_WALK_TIME_MAX)
        self.__timer = 0

    def enter(self, **kwargs):
        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]

        angle = atan2(
            owner.bounding_box.centery - opponent.bounding_box.centery,
            opponent.bounding_box.centerx - owner.bounding_box.centerx
        )
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
            return states.ai.idle_state.IdleState()

        owner_bbox = owner.bounding_box
        opponent_bbox = opponent.bounding_box
        dist_x = abs(opponent_bbox.centerx - owner_bbox.centerx)
        dist_y = abs(opponent_bbox.centery - owner_bbox.centery)
        if ((owner_bbox.left <= opponent_bbox.left <= owner_bbox.right or
                owner_bbox.left <= opponent_bbox.right <= owner_bbox.right) and
                (owner_bbox.top <= opponent_bbox.top <= owner_bbox.bottom or
                owner_bbox.top <= opponent_bbox.bottom <= owner_bbox.bottom) or
                sqrt(dist_x ** 2 + dist_y ** 2) <= ENEMY_ATTACK_INITIATION_DISTANCE):
            return states.ai.idle_state.IdleState()

        return None

    def handle_event(self, **kwargs):
        event = kwargs["event"]

        match event.__class__:
            case events.MovementObstructed:
                return states.ai.idle_state.IdleState()
            case events.WasDefeated:
                return states.character.dying_state.DyingState()

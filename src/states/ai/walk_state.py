from math import atan2, pi, sqrt
from random import randint

from direction import direction
from game import events
import states.state
import states.ai.idle_state   # pylint: disable=cyclic-import
import states.character.dying_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).

class WalkState(states.state.State):
    """Walking state for the finite state machine that implements enemy AI."""

    def __init__(self):
        self.__duration = None
        self.__timer = None

    def enter(self, **kwargs):
        """Called right after transitioning to this state.

        Args:
            owner: The Character instance that this state belongs to.
            opponents: A list containing only the player Character instance.
            config: The AiConfig instance of the game.
        """

        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]
        config = kwargs["config"]

        self.__duration = randint(config.walk_time.minimum, config.walk_time.maximum)
        self.__timer = 0

        owner.direction.moving = self.__get_direction_toward_opponent(owner, opponent)

    def __get_direction_toward_opponent(self, owner, opponent):
        angle = atan2(
            owner.bounding_box.centery - opponent.bounding_box.centery,
            opponent.bounding_box.centerx - owner.bounding_box.centerx
        )

        if -7*pi/8 <= angle < -5*pi/8:
            direction_toward_opponent = direction.DOWN_LEFT
        elif -5*pi/8 <= angle < -3*pi/8:
            direction_toward_opponent = direction.DOWN
        elif -3*pi/8 <= angle < -pi/8:
            direction_toward_opponent = direction.DOWN_RIGHT
        elif -pi/8 <= angle < pi/8:
            direction_toward_opponent = direction.RIGHT
        elif pi/8 <= angle < 3*pi/8:
            direction_toward_opponent = direction.UP_RIGHT
        elif 3*pi/8 <= angle < 5*pi/8:
            direction_toward_opponent = direction.UP
        elif 5*pi/8 <= angle < 7*pi/8:
            direction_toward_opponent = direction.UP_LEFT
        else:
            direction_toward_opponent = direction.LEFT

        return direction_toward_opponent

    def update(self, **kwargs):
        """Called once each game loop iteration.

        Args:
            dt: Time elapsed since the last game loop iteration in milliseconds.
            owner: The Character instance that this state belongs to.
            opponents: A list containing only the player Character instance.
            config: The AiConfig instance of the game.

        Returns:
            A new state that the Character should now transition to or None.
        """

        dt = kwargs["dt"]
        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]
        config = kwargs["config"]

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
                sqrt(dist_x ** 2 + dist_y ** 2) <= config.attack_initiation_distance):
            return states.ai.idle_state.IdleState()

        return None

    def handle_event(self, **kwargs):
        """Called when the Character that owns this state receives a game event.

        Args:
            event: Event object of one of the classes from the "events" module.

        Returns:
            A new state that the Character should now transition to or None.
        """

        event = kwargs["event"]

        match event.__class__:
            case events.MovementObstructed:
                return states.ai.idle_state.IdleState()
            case events.WasDefeated:
                return states.character.dying_state.DyingState()

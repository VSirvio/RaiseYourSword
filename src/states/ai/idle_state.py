from math import sqrt
from random import randrange

from direction import direction
from game import events
import states.state
import states.ai.attack_state   # pylint: disable=cyclic-import
import states.ai.walk_state   # pylint: disable=cyclic-import
import states.character.dying_state   # pylint: disable=cyclic-import
import states.character.perpetual_idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).

class IdleState(states.state.State):
    """Idle state for the finite state machine that implements enemy AI."""

    def __init__(self):
        self.__duration = None
        self.__timer = None

    def enter(self, **kwargs):
        """Called right after transitioning to this state.

        Args:
            owner: The Character instance that this state belongs to.
            config: The AiConfig instance of the game.
        """

        owner = kwargs["owner"]
        config = kwargs["config"]

        self.__duration = randrange(config.idle_time.minimum, config.idle_time.maximum)
        self.__timer = 0

        owner.direction.moving = direction.NONE

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

        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]
        config = kwargs["config"]

        self.__timer += kwargs["dt"]

        owner_bbox = owner.bounding_box
        opponent_bbox = opponent.bounding_box
        dist_x = abs(opponent_bbox.centerx - owner_bbox.centerx)
        dist_y = abs(opponent_bbox.centery - owner_bbox.centery)
        bounding_boxes_touching = ((owner_bbox.left <= opponent_bbox.left <= owner_bbox.right or
            owner_bbox.left <= opponent_bbox.right <= owner_bbox.right) and
            (owner_bbox.top <= opponent_bbox.top <= owner_bbox.bottom or
            owner_bbox.top <= opponent_bbox.bottom <= owner_bbox.bottom))
        if (opponent.state not in ("dead", "dying") and (bounding_boxes_touching or
                sqrt(dist_x ** 2 + dist_y ** 2) <= config.attack_initiation_distance)):
            return states.ai.attack_state.AttackState()

        if self.__timer >= self.__duration:
            return states.ai.walk_state.WalkState()

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
            case events.GameEnded:
                return states.character.perpetual_idle_state.PerpetualIdleState()
            case events.WasDefeated:
                return states.character.dying_state.DyingState()

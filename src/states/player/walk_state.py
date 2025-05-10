from direction import direction
from game import events
import states.state
import states.player.attack_state   # pylint: disable=cyclic-import
import states.player.idle_state   # pylint: disable=cyclic-import
import states.character.dying_state   # pylint: disable=cyclic-import
import states.character.perpetual_idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class WalkState(states.state.State):
    """Walking state for the player character."""

    def __init__(self, walk_direction):
        """Creates a walk state with the given direction.

        Args:
            walk_direction: A Direction instance.
        """

        self.__direction = walk_direction

    def enter(self, **kwargs):
        """Called right after transitioning to this state.

        Args:
            owner: The Character instance of the player character.
        """

        owner = kwargs["owner"]

        owner.direction.moving = self.__direction

    def handle_event(self, **kwargs):
        """Called when the player character receives a game event.

        Args:
            event: Event object of one of the classes from the "events" module.

        Returns:
            A new state that the player should now transition to or None.
        """

        event = kwargs["event"]

        match event.__class__:
            case events.AttackStarted:
                return states.player.attack_state.AttackState()
            case events.WasDefeated:
                return states.character.dying_state.DyingState()
            case events.MovementDirectionChanged:
                if event.new_direction == direction.NONE:
                    return states.player.idle_state.IdleState()
                return WalkState(event.new_direction)
            case events.GameEnded:
                return states.character.perpetual_idle_state.PerpetualIdleState()

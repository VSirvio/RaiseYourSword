from direction import direction
from game import events
import states.state
import states.character.dying_state   # pylint: disable=cyclic-import
import states.character.perpetual_idle_state   # pylint: disable=cyclic-import
import states.player.attack_state   # pylint: disable=cyclic-import
import states.player.walk_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class IdleState(states.state.State):
    """Idle state for the player character."""

    def enter(self, **kwargs):
        """Called right after transitioning to this state.

        Args:
            owner: The Character instance of the player character.
        """

        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

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
            case events.MovementDirectionChanged:
                return states.player.walk_state.WalkState(event.new_direction)
            case events.WasDefeated:
                return states.character.dying_state.DyingState()
            case events.GameEnded:
                return states.character.perpetual_idle_state.PerpetualIdleState()

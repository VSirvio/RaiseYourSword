from direction import direction
from game import events
import states.state
import states.character.dead_state

class DyingState(states.state.State):
    """Dying state for the finite state machines used by the characters."""

    def enter(self, **kwargs):
        """Called right after transitioning to this state.

        Args:
            owner: The Character instance that this state belongs to.
        """

        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

    def handle_event(self, **kwargs):
        """Called when the Character that owns this state receives a game event.

        Args:
            event: Event object of one of the classes from the "events" module.

        Returns:
            A new state that the Character should now transition to or None.
        """

        event = kwargs["event"]

        match event.__class__:
            case events.AnimationFinished:
                return states.character.dead_state.DeadState()

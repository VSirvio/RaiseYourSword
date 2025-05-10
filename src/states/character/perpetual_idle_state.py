from direction import direction
import states.state

class PerpetualIdleState(states.state.State):
    """Idle state in which characters are when ending screen is shown."""

    @property
    def type(self):
        """Returns "idle" so that the idle animation is shown."""

        return "idle"

    def enter(self, **kwargs):
        """Called right after transitioning to this state.

        Args:
            owner: The Character instance that this state belongs to.
        """

        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

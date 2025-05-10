from direction.direction import NONE, DOWN, UP, RIGHT, LEFT
from game import events
import states.state
import states.ai.idle_state   # pylint: disable=cyclic-import
import states.character.dying_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).

class AttackState(states.state.State):
    """Attack state for the finite state machine that implements enemy AI."""

    def enter(self, **kwargs):
        """Called right after transitioning to this state.

        Args:
            owner: The Character instance that this state belongs to.
            opponents: A list containing only the player Character instance.
        """

        owner = kwargs["owner"]
        opponent = kwargs["opponents"][0]

        owner_bbox = owner.bounding_box
        opponent_bbox = opponent.bounding_box
        if owner_bbox.bottom <= opponent_bbox.top and owner_bbox.right > opponent_bbox.left:
            owner.direction.moving = DOWN
        elif owner_bbox.left >= opponent_bbox.right and owner_bbox.bottom > opponent_bbox.top:
            owner.direction.moving = LEFT
        elif owner_bbox.top >= opponent_bbox.bottom and owner_bbox.left < opponent_bbox.right:
            owner.direction.moving = UP
        else:
            owner.direction.moving = RIGHT

        owner.direction.moving = NONE

    def handle_event(self, **kwargs):
        """Called when the Character that owns this state receives a game event.

        Args:
            event: Event object of one of the classes from the "events" module.
            owner: The Character instance that this state belongs to.
            opponents: A list containing only the player Character instance.

        Returns:
            A new state that the Character should now transition to or None.
        """

        event = kwargs["event"]
        owner = kwargs["owner"] if event.__class__ == events.DealingDamage else None
        opponent = kwargs["opponents"][0] if event.__class__ == events.DealingDamage else None

        match event.__class__:
            case events.AnimationFinished:
                return states.ai.idle_state.IdleState()
            case events.DealingDamage:
                if owner.does_attack_hit(opponent):
                    opponent.defeat()
            case events.WasDefeated:
                return states.character.dying_state.DyingState()

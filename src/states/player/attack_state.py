from direction import direction
from game import events
import states.state
import states.player.idle_state   # pylint: disable=cyclic-import
import states.character.dying_state   # pylint: disable=cyclic-import
import states.character.perpetual_idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class AttackState(states.state.State):
    """Attack state for the player character."""

    def __init__(self):
        self.__last_enemy_is_dying = False

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
            owner: The Character instance of the player character.
            opponents: List of the Character instances of the enemy characters.

        Returns:
            A new state that the player should now transition to or None.
        """

        event = kwargs["event"]
        if event.__class__ in (events.AnimationFinished, events.DealingDamage):
            owner = kwargs["owner"]
            opponents = kwargs["opponents"]
        else:
            owner = None
            opponents = None

        match event.__class__:
            case events.AnimationFinished:
                if self.__last_enemy_is_dying:
                    return states.character.perpetual_idle_state.PerpetualIdleState()
                if owner.direction.controlled_toward == direction.NONE:
                    return states.player.idle_state.IdleState()
                return states.player.walk_state.WalkState(owner.direction.controlled_toward)
            case events.DealingDamage:
                hits_all_remaining_enemies = True
                for opponent in opponents:
                    if owner.does_attack_hit(opponent):
                        opponent.defeat()
                    elif opponent.state not in ("dead", "dying"):
                        hits_all_remaining_enemies = False
                self.__last_enemy_is_dying = hits_all_remaining_enemies
            case events.WasDefeated:
                return states.character.dying_state.DyingState()

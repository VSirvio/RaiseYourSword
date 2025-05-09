from direction import direction
from game import events
import states.state
import states.player.dying_state   # pylint: disable=cyclic-import
import states.player.idle_state   # pylint: disable=cyclic-import
import states.player.perpetual_idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class AttackState(states.state.State):
    def __init__(self):
        self.__last_enemy_is_dying = False

    def enter(self, **kwargs):
        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

    def handle_event(self, **kwargs):
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
                    return states.player.perpetual_idle_state.PerpetualIdleState()
                if owner.direction.controlled_toward == direction.NONE:
                    return states.player.idle_state.IdleState()
                return states.player.walk_state.WalkState(owner.direction.controlled_toward)
            case events.DealingDamage:
                for opponent in opponents:
                    if owner.does_attack_hit(opponent):
                        opponent.defeat()
            case events.WasDefeated:
                return states.player.dying_state.DyingState()
            case events.LastEnemyDying:
                self.__last_enemy_is_dying = True

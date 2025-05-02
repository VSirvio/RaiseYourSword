import direction
import events
import state
import states.dying_state   # pylint: disable=cyclic-import
import states.idle_state   # pylint: disable=cyclic-import
import states.walk_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class AttackState(state.State):
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
                if owner.direction.controlled_toward == direction.NONE:
                    return states.idle_state.IdleState()
                return states.walk_state.WalkState(owner.direction.controlled_toward)
            case events.DealingDamage:
                for opponent in opponents:
                    if owner.does_attack_hit(opponent):
                        opponent.defeat()
            case events.WasDefeated:
                return states.dying_state.DyingState()

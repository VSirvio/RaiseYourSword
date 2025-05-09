from direction import direction
from game import events
import states.state
import states.player.attack_state   # pylint: disable=cyclic-import
import states.player.dying_state   # pylint: disable=cyclic-import
import states.player.idle_state   # pylint: disable=cyclic-import
import states.player.perpetual_idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class WalkState(states.state.State):
    def __init__(self, walk_direction):
        self.__direction = walk_direction

    def enter(self, **kwargs):
        owner = kwargs["owner"]

        owner.direction.moving = self.__direction

    def handle_event(self, **kwargs):
        event = kwargs["event"]

        match event.__class__:
            case events.AttackStarted:
                return states.player.attack_state.AttackState()
            case events.WasDefeated:
                return states.player.dying_state.DyingState()
            case events.MovementDirectionChanged:
                if event.new_direction == direction.NONE:
                    return states.player.idle_state.IdleState()
                return WalkState(event.new_direction)
            case events.GameEnded:
                return states.player.perpetual_idle_state.PerpetualIdleState()

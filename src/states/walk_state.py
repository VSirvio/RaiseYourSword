import direction
import events
import state
import states.attack_state   # pylint: disable=cyclic-import
import states.idle_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class WalkState(state.State):
    def __init__(self, walk_direction):
        self.__direction = walk_direction

    def enter(self, **kwargs):
        player = kwargs["player"]

        player.direction.moving = self.__direction

    def update(self, **kwargs):
        return None

    def handle_event(self, **kwargs):
        event = kwargs["event"]

        match event.__class__:
            case events.AttackStarted:
                return states.attack_state.AttackState()
            case events.MovementDirectionChanged:
                if event.new_direction == direction.NONE:
                    return states.idle_state.IdleState()
                return WalkState(event.new_direction)
            case events.Lose:
                return states.idle_state.IdleState()

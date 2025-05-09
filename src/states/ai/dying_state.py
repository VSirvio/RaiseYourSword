from direction import direction
from game import events
import states.state
import states.ai.dead_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing game AIs. It often requires
# transitions like state1->state2->state1, and for that reason it is necessary to use cyclic
# imports (like in the example given, state1 would need to import state2 and state2 would also need
# to import state1).

class DyingState(states.state.State):
    def enter(self, **kwargs):
        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

    def handle_event(self, **kwargs):
        event = kwargs["event"]

        match event.__class__:
            case events.AnimationFinished:
                return states.ai.dead_state.DeadState()

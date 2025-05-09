from direction import direction
from game import events
import states.state
import states.character.dead_state

class DyingState(states.state.State):
    def enter(self, **kwargs):
        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

    def handle_event(self, **kwargs):
        event = kwargs["event"]

        match event.__class__:
            case events.AnimationFinished:
                return states.character.dead_state.DeadState()

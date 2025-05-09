from direction import direction
import states.state

class PerpetualIdleState(states.state.State):
    @property
    def type(self):
        return "idle"

    def enter(self, **kwargs):
        owner = kwargs["owner"]

        owner.direction.moving = direction.NONE

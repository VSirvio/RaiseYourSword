import direction
import events
import state
import states.idle_state   # pylint: disable=cyclic-import
import states.walk_state   # pylint: disable=cyclic-import
# "State" design pattern is a well-known best practice for implementing animation state management
# in games. It often requires transitions like state1->state2->state1, and for that reason it is
# necessary to use cyclic imports (like in the example given, state1 would need to import state2
# and state2 would also need to import state1).

class AttackState(state.State):
    def enter(self, **kwargs):
        player = kwargs["player"]
        enemy = kwargs["enemy"]

        player.movement_direction = direction.NONE

        if player.does_attack_hit(enemy):
            enemy.fall()

    def handle_event(self, **kwargs):
        event = kwargs["event"]
        player = kwargs["player"]

        match event.__class__:
            case events.AnimationFinished:
                enemy = kwargs["enemy"]
                if enemy.has_been_defeated or player.direction_controlled_toward == direction.NONE:
                    return states.idle_state.IdleState()
                return states.walk_state.WalkState(player.direction_controlled_toward)
            case events.Lose:
                return states.idle_state.IdleState()

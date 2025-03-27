class AttackState:
    def enter(self, sprite):
        sprite.attack()

    def handle_input(self, event, key_pressed):
        return None

    def animation_finished(self):
        return IdleState()

    def __str__(self):
        return "attack"

from states.idle_state import IdleState

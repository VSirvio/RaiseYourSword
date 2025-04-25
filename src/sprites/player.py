import events
import sprites.character
import states.idle_state

class Player(sprites.character.Character):
    def __init__(self, weapon_hitbox, starting_position, direction, animations, physics):
        super().__init__(states.idle_state.IdleState())

        self._has_been_defeated = False

        self.direction = direction

        self.__animations = animations
        self.image = self.__animations.current_frame(self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = starting_position

        self.__weapon_hitbox = weapon_hitbox

        self.__physics = physics

    def __update_state(self, state, enemy):
        if state is not None:
            self._state = state
            self._state.enter(player=self, enemy=enemy)
            self.__animations.reset(self)

    def update(self, dt, **kwargs):
        enemy = kwargs["enemy"]

        self.__update_state(self._state.update(dt=dt, player=self, enemy=enemy), enemy)

        self.__animations.update(dt, self, enemy)
        self.image = self.__animations.current_frame(self)

        self.__physics.update(dt, self, enemy)

    def handle_event(self, event, enemy):
        if event.__class__ == events.MovementDirectionChanged:
            self.direction.controlled_toward = event.new_direction

        new_state = self._state.handle_event(player=self, enemy=enemy, event=event)
        self.__update_state(new_state, enemy)

    def does_attack_hit(self, enemy):
        current_weapon_hitbox = self.__weapon_hitbox[self.direction.facing]
        weapon_hitbox_relative_to_screen = current_weapon_hitbox.move(self.rect.x, self.rect.y)
        return weapon_hitbox_relative_to_screen.colliderect(enemy.bounding_box)

    @property
    def bounding_box(self):
        return self.__physics.bounding_box.move(self.rect.x, self.rect.y)

    @property
    def has_been_defeated(self):
        return self._has_been_defeated

    def lose(self):
        self._has_been_defeated = True

        new_state = self._state.handle_event(player=self, event=events.Lose())
        self.__update_state(new_state, None)

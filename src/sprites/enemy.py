import ai.idle_state
import sprites.character

class Enemy(sprites.character.Character):
    def __init__(self, weapon_hitbox, starting_position, direction, animations, physics):
        super().__init__(ai.idle_state.IdleState())

        self._has_been_defeated = False

        self.direction = direction

        self.__animations = animations
        self.image = self.__animations.current_frame(self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = starting_position

        self.__weapon_hitbox = weapon_hitbox

        self.__physics = physics

    def __update_state(self, state, player):
        if state is not None:
            self._state = state
            self._state.enter(enemy=self, player=player)
            self.__animations.reset(self)

    def update(self, dt, **kwargs):
        player = kwargs["player"]

        self.__update_state(self._state.update(dt=dt, enemy=self, player=player), player)

        self.__animations.update(dt, self, player)
        self.image = self.__animations.current_frame(self)

        self.__physics.update(dt, self)

    def handle_event(self, event, player):
        new_state = self._state.handle_event(event)
        self.__update_state(new_state, player)

    def does_attack_hit(self, player):
        current_weapon_hitbox = self.__weapon_hitbox[self.direction.facing]
        weapon_hitbox_relative_to_screen = current_weapon_hitbox.move(self.rect.x, self.rect.y)
        return weapon_hitbox_relative_to_screen.colliderect(player.bounding_box)

    @property
    def bounding_box(self):
        return self.__physics.bounding_box.move(self.rect.x, self.rect.y)

    @property
    def has_been_defeated(self):
        return self._has_been_defeated

    def fall(self):
        self._has_been_defeated = True

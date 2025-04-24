from direction import NONE
import events
import sprites.character
import states.idle_state

class Player(sprites.character.Character):
    def __init__(self, animations, weapon_hitbox, starting_position, physics):
        super().__init__(animations, states.idle_state.IdleState())

        self._has_been_defeated = False

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = starting_position

        self.__weapon_hitbox = weapon_hitbox

        self.__direction_controlled_toward = NONE

        self.__physics = physics

    def __update_state(self, state, enemy):
        if state is not None:
            self._state = state
            self._state.enter(player=self, enemy=enemy)

    def update(self, dt, **kwargs):
        enemy = kwargs["enemy"]

        super().update(dt)

        frametime = 1000 / self._animations[self._state.type]["framerate"]
        while self._timer >= frametime:
            self._index = self._next_index()

            if self._index == 0:
                event = events.AnimationFinished()
                new_state = self._state.handle_event(player=self, enemy=enemy, event=event)
                self.__update_state(new_state, enemy)

            self._timer -= frametime

        self.image = self._animations[self._state.type][self._facing_direction][self._index]

        self.__physics.update(dt, self, enemy)

    def handle_event(self, event, enemy):
        if event.__class__ == events.MovementDirectionChanged:
            self.__direction_controlled_toward = event.new_direction

        new_state = self._state.handle_event(player=self, enemy=enemy, event=event)
        self.__update_state(new_state, enemy)

    def attack(self, enemy):
        self.movement_direction = NONE

        current_weapon_hitbox = self.__weapon_hitbox[self._facing_direction]
        weapon_hitbox_relative_to_screen = current_weapon_hitbox.move(self.rect.x, self.rect.y)
        if weapon_hitbox_relative_to_screen.colliderect(enemy.bounding_box):
            enemy.fall()

    @property
    def direction_controlled_toward(self):
        return self.__direction_controlled_toward

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

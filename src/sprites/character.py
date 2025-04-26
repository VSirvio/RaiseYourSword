import pygame

import events

class Character(pygame.sprite.Sprite):
    def __init__(self, role, weapon_hitbox, initial_state, starting_position, direction,
            animations, physics):
        super().__init__()

        self._has_been_defeated = False

        self.__role = role

        self._state = initial_state

        self.direction = direction

        self.__animations = animations
        self.image = self.__animations.current_frame(self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = starting_position

        self.__weapon_hitbox = weapon_hitbox

        self.__physics = physics

    def __update_state(self, state, opponent):
        if state is not None:
            self._state = state
            self._state.enter(owner=self, opponent=opponent)
            self.__animations.reset(self)

    def update(self, dt, opponent_to):
        opponent = opponent_to[self.__role]

        self.__update_state(self._state.update(dt=dt, owner=self, opponent=opponent), opponent)

        self.__animations.update(dt, self, opponent)
        self.image = self.__animations.current_frame(self)

        self.__physics.update(dt, self, opponent)

    def handle_event(self, event, opponent):
        self.direction.handle(event)

        new_state = self._state.handle_event(owner=self, opponent=opponent, event=event)
        self.__update_state(new_state, opponent)

    def does_attack_hit(self, opponent):
        current_weapon_hitbox = self.__weapon_hitbox[self.direction.facing]
        weapon_hitbox_relative_to_screen = current_weapon_hitbox.move(self.rect.x, self.rect.y)
        return weapon_hitbox_relative_to_screen.colliderect(opponent.bounding_box)

    @property
    def bounding_box(self):
        return self.__physics.bounding_box.move(self.rect.x, self.rect.y)

    @property
    def has_been_defeated(self):
        return self._has_been_defeated

    def defeat(self):
        self._has_been_defeated = True

        new_state = self._state.handle_event(event=events.WasDefeated())
        self.__update_state(new_state, None)

    @property
    def state(self):
        return self._state.type

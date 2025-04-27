import events
from sprites.custom_sprite import CustomSprite

class Character:
    def __init__(self, *, role, initial_state, starting_position, direction, animations, physics):
        super().__init__()

        self._has_been_defeated = False

        self.__role = role

        self._state = initial_state

        self.direction = direction

        self.__sprite = CustomSprite(self)

        self.__animations = animations
        self.__sprite.image = self.__animations.current_frame(self)

        self.__sprite.rect = self.__sprite.image.get_rect()
        self.__sprite.rect.x, self.__sprite.rect.y = starting_position

        self.__physics = physics

    def __update_state(self, state, opponents):
        if state is not None:
            self._state = state
            self._state.enter(owner=self, opponents=opponents)
            self.__animations.reset()
            self.__sprite.image = self.__animations.current_frame(self)

    def update(self, dt, opponents_to):
        opponents = opponents_to[self.__role]

        self.__update_state(self._state.update(dt=dt, owner=self, opponents=opponents), opponents)

        self.__animations.update(dt, self, opponents)
        self.__sprite.image = self.__animations.current_frame(self)

        self.__physics.update(dt, self, opponents)

    def handle_event(self, event, opponents):
        self.direction.handle(event)

        new_state = self._state.handle_event(owner=self, opponents=opponents, event=event)
        self.__update_state(new_state, opponents)

    def does_attack_hit(self, opponents):
        return self.__physics.does_attack_hit(attacker=self, target=opponents)

    @property
    def sprite(self):
        return self.__sprite

    @property
    def x(self):
        return self.__sprite.rect.x

    @x.setter
    def x(self, x):
        self.__sprite.rect.x = x

    @property
    def y(self):
        return self.__sprite.rect.y

    @y.setter
    def y(self, y):
        self.__sprite.rect.y = y

    @property
    def width(self):
        return self.__sprite.rect.width

    @property
    def height(self):
        return self.__sprite.rect.height

    @property
    def bounding_box(self):
        return self.__physics.bounding_box.move(self.x, self.y)

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

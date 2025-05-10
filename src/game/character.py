from . import events
from .custom_sprite import CustomSprite

class Character:
    """Represents a character in the game (e.g. player or enemy).

    Attributes:
        direction: A CharacterDirection instance or instance of its subclass.
    """

    def __init__(self, *, initial_state, starting_position, direction, animations, physics,
            config=None):
        """Creates a new character with the given parameters.

        Args:
            initial_state: An instance of a state.State subclass.
            starting_position: A tuple of the form (X coordinate, Y coordinate).
            direction: A CharacterDirection (or its subclass) instance.
            animations: An AnimationsComponent (or its subclass) instance.
            physics: A PhysicsComponent (or its subclass) instance.
        """

        super().__init__()

        self.direction = direction

        self.__state = initial_state
        self.__state.enter(owner=self, opponents=[], config=config)

        self.__sprite = CustomSprite(self)

        self.__animations = animations
        self.__sprite.image = self.__animations.current_frame(self)

        self.__sprite.rect = self.__sprite.image.get_rect()
        self.__sprite.rect.x, self.__sprite.rect.y = starting_position

        self.__physics = physics

    def __update_state(self, state, opponents, config=None):
        if state is not None:
            self.__state = state
            self.__state.enter(owner=self, opponents=opponents, config=config)
            self.__animations.reset()
            self.__sprite.image = self.__animations.current_frame(self)

    def update(self, dt, opponents, other_characters, config=None):
        """Updates game logic that is directly related to the player.

        Args:
            dt: The time elapsed from the last call in milliseconds.
            opponents: A list of Character objects (usually enemies or player).
            other_characters: [] for the player and other enemies for an enemy.
        """

        new_state = self.__state.update(dt=dt, owner=self, opponents=opponents, config=config)
        self.__update_state(new_state, opponents, config)

        self.__animations.update(dt, self, opponents, config)
        self.__sprite.image = self.__animations.current_frame(self)

        self.__physics.update(dt, self, opponents, other_characters, config)

    def handle_event(self, event, opponents, config=None):
        """Handles a game event.

        Args:
            event: Event object of one of the classes from the "events" module.
            opponents: A list of Character objects (usually enemies or player).
        """

        self.direction.handle(event)

        new_state = self.__state.handle_event(event=event, owner=self, opponents=opponents,
            config=config)
        self.__update_state(new_state, opponents, config)

    def does_attack_hit(self, target):
        """Checks if an attack by the character hits the target.

        Args:
            target: A Character instance.

        Returns:
            A boolean value indicating whether the attack hits.
        """

        return self.__physics.does_attack_hit(attacker=self, target=target)

    @property
    def sprite(self):
        """The pygame.sprite.Sprite related to the character."""

        return self.__sprite

    @property
    def x(self):
        """X coordinate of the top left corner of the sprite on the screen."""

        return self.__sprite.rect.x

    @x.setter
    def x(self, x):
        self.__sprite.rect.x = x

    @property
    def y(self):
        """Y coordinate of the top left corner of the sprite on the screen."""

        return self.__sprite.rect.y

    @y.setter
    def y(self, y):
        self.__sprite.rect.y = y

    @property
    def width(self):
        """The width of the character sprite."""

        return self.__sprite.rect.width

    @property
    def height(self):
        """The height of the character sprite."""

        return self.__sprite.rect.height

    @property
    def bounding_box(self):
        """A pygame.Rect representing the physical size of the character."""

        return self.__physics.bounding_box.move(self.x, self.y)

    @property
    def character_hitbox(self):
        """A pygame.Rect representing the hittable area of the character."""

        return self.__physics.character_hitbox.move(self.x, self.y)

    def defeat(self):
        """Defeats this character."""

        new_state = self.__state.handle_event(event=events.WasDefeated())
        self.__update_state(new_state, None)

    @property
    def state(self):
        """A string indicating the type of the current state."""

        return self.__state.type

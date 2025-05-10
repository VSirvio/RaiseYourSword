from game import events

class AnimationsComponent:
    """Responsible of animation logic of a Character."""

    def __init__(self, animations):
        """Creates an animation component with the given animations.

        Args:
            animations: A CharacterAnimation instance.
        """

        self.__animations = animations
        self.__index = 0
        self.__timer = 0

    def update(self, dt, owner, opponents, config):
        """Update method to be called each game loop iteration.

        Args:
            dt: Time passed since the last game loop iteration in milliseconds.
            owner: A Character instance that owns this component.
            opponents: List of Character instances that are opponents to owner.
            config: Optional character configuration data.
        """

        self.__timer += dt

        current_animation = self.__animations[owner.state][owner.direction.facing]

        frametime = 1000 / current_animation.framerate
        while self.__timer >= frametime:
            num_of_frames = len(current_animation.frames)
            self.__index = (self.__index + 1) % num_of_frames

            if self.__index == 0:
                owner.handle_event(events.AnimationFinished(), opponents, config)

            if owner.state == "attack" and self.__index in current_animation.damage_frames:
                owner.handle_event(events.DealingDamage(), opponents)

            self.__timer -= frametime

    def current_frame(self, owner):
        """The current frame in the current animation.

        Args:
            owner: A Character instance that owns this component.

        Returns:
            A pygame Surface containing the current animation frame.
        """

        return self.__animations[owner.state][owner.direction.facing].frames[self.__index]

    def reset(self):
        """Resets the current animation back to the start."""

        self.__index = 0
        self.__timer = 0

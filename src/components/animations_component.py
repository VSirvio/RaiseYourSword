from game import events

class AnimationsComponent:
    def __init__(self, animations):
        self.__animations = animations
        self.__index = 0
        self.__timer = 0

    def update(self, dt, owner, opponents):
        self.__timer += dt

        current_animation = self.__animations[owner.state][owner.direction.facing]

        frametime = 1000 / current_animation.framerate
        while self.__timer >= frametime:
            num_of_frames = len(current_animation.frames)
            self.__index = (self.__index + 1) % num_of_frames

            if self.__index == 0:
                owner.handle_event(events.AnimationFinished(), opponents)

            if owner.state == "attack" and self.__index in current_animation.damage_frames:
                owner.handle_event(events.DealingDamage(), opponents)

            self.__timer -= frametime

    def current_frame(self, owner):
        return self.__animations[owner.state][owner.direction.facing].frames[self.__index]

    def reset(self):
        self.__index = 0
        self.__timer = 0

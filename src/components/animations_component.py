import events

class AnimationsComponent:
    def __init__(self, animations):
        self.__animations = animations
        self.__index = 0
        self.__timer = 0

    def update(self, dt, owner, opponents):
        self.__timer += dt

        frametime = 1000 / self.__animations[owner.state]["framerate"]
        while self.__timer >= frametime:
            num_of_frames = len(self.__animations[owner.state][owner.direction.facing])
            self.__index = (self.__index + 1) % num_of_frames

            if self.__index == 0:
                owner.handle_event(events.AnimationFinished(), opponents)

            self.__timer -= frametime

    def current_frame(self, owner):
        return self.__animations[owner.state][owner.direction.facing][self.__index]

    def reset(self):
        self.__index = 0
        self.__timer = 0

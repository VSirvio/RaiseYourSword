import events

class PlayerAnimations:
    def __init__(self, animations):
        self.__animations = animations
        self.__index = 0
        self.__timer = 0

    def update(self, dt, player, enemy):
        self.__timer += dt

        frametime = 1000 / self.__animations[player.state]["framerate"]
        while self.__timer >= frametime:
            num_of_frames = len(self.__animations[player.state][player.facing_direction])
            self.__index = (self.__index + 1) % num_of_frames

            if self.__index == 0:
                player.handle_event(events.AnimationFinished(), enemy)

            self.__timer -= frametime

    def current_frame(self, player):
        return self.__animations[player.state][player.facing_direction][self.__index]

    def reset(self, player):
        self.__index = 0
        player.image = self.current_frame(player)
        self.__timer = 0

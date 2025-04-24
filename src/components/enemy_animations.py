import events

class EnemyAnimations:
    def __init__(self, animations):
        self.__animations = animations
        self.__index = 0
        self.__timer = 0

    def update(self, dt, enemy, player):
        self.__timer += dt

        frametime = 1000 / self.__animations[enemy.state]["framerate"]
        while self.__timer >= frametime:
            num_of_frames = len(self.__animations[enemy.state][enemy.facing_direction])
            self.__index = (self.__index + 1) % num_of_frames

            if self.__index == 0:
                enemy.handle_event(events.AnimationFinished(), player)

            self.__timer -= frametime

    def current_frame(self, enemy):
        return self.__animations[enemy.state][enemy.facing_direction][self.__index]

    def reset(self, enemy):
        self.__index = 0
        enemy.image = self.current_frame(enemy)
        self.__timer = 0

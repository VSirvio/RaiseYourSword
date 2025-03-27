import pygame

class GameLoop:
    def __init__(self, game, renderer, event_queue, clock):
        self.__game = game
        self.__renderer = renderer
        self.__event_queue = event_queue
        self.__clock = clock

        self.__dt = 0

        self.__key_pressed = {"down": False, "up": False, "left": False, "right": False}

    def start(self):
        while True:
            if not self.__handle_events():
                break

            self.__update()

            self.__renderer.render()

            self.__dt = self.__clock.tick(60)

    def __handle_events(self):
        for event in self.__event_queue.get():
            if event.type == pygame.QUIT:
                return False

            if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
                continue

            match event.key:
                case pygame.K_DOWN | pygame.K_s:
                    self.__key_pressed["down"] = event.type == pygame.KEYDOWN
                case pygame.K_UP | pygame.K_w:
                    self.__key_pressed["up"] = event.type == pygame.KEYDOWN
                case pygame.K_LEFT | pygame.K_a:
                    self.__key_pressed["left"] = event.type == pygame.KEYDOWN
                case pygame.K_RIGHT | pygame.K_d:
                    self.__key_pressed["right"] = event.type == pygame.KEYDOWN

            self.__game.handle_input(event, self.__key_pressed)

        return True

    def __update(self):
        self.__game.update(self.__dt)

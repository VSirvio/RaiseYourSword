import pygame

class GameLoop:
    def __init__(self, game, renderer, event_queue, clock):
        self.__game = game
        self.__renderer = renderer
        self.__event_queue = event_queue
        self.__clock = clock

        self.__dt = 0

        self.__key_pressed = {"down": False, "up": False, "left": False, "right": False}

        self.__vert_direction = None
        self.__horiz_direction = None

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

            if event.type not in (pygame.KEYDOWN, pygame.KEYUP) or self.__game.finished:
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
                case pygame.K_RSHIFT | pygame.K_LSHIFT if event.type == pygame.KEYDOWN:
                    self.__game.attack()

        if self.__game.finished:
            self.__vert_direction = None
            self.__horiz_direction = None
            return True

        self.__vert_direction = None
        if self.__key_pressed["up"] and not self.__key_pressed["down"]:
            self.__vert_direction = "up"
        elif self.__key_pressed["down"] and not self.__key_pressed["up"]:
            self.__vert_direction = "down"

        self.__horiz_direction = None
        if self.__key_pressed["left"] and not self.__key_pressed["right"]:
            self.__horiz_direction = "left"
        elif self.__key_pressed["right"] and not self.__key_pressed["left"]:
            self.__horiz_direction = "right"

        return True

    def __update(self):
        self.__game.walk(self.__vert_direction, self.__horiz_direction)

        self.__game.update(self.__dt)

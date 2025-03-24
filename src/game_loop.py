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
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.__key_pressed["down"] = True
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.__key_pressed["up"] = True
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.__key_pressed["left"] = True
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.__key_pressed["right"] = True
                elif event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
                    self.__game.attack()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.__key_pressed["down"] = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.__key_pressed["up"] = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.__key_pressed["left"] = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.__key_pressed["right"] = False
            elif event.type == pygame.QUIT:
                return False

        self.__vert_direction = None
        if self.__key_pressed["up"]:
            if self.__key_pressed["down"]:
                self.__vert_direction = None
            else:
                self.__vert_direction = "up"
        elif self.__key_pressed["down"]:
            self.__vert_direction = "down"

        self.__horiz_direction = None
        if self.__key_pressed["left"]:
            if self.__key_pressed["right"]:
                self.__horiz_direction = None
            else:
                self.__horiz_direction = "left"
        elif self.__key_pressed["right"]:
            self.__horiz_direction = "right"

        return True

    def __update(self):
        self.__game.walk(self.__vert_direction, self.__horiz_direction)

        self.__game.update(self.__dt)

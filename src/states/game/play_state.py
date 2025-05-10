import pygame

from game import events
from game.enemy_spawner import EnemySpawner
import states.game.defeat_screen_state
import states.game.victory_screen_state

class PlayState:
    def __init__(self):
        self.__spawner = None
        self.__sprite_group = None

    def enter(self, game):
        self.__spawner = EnemySpawner(game)
        self.__sprite_group = pygame.sprite.Group()

    def update(self, *args):
        dt = args[0]
        game = args[1]

        self.__spawner.spawn_enemies(dt, game)

    def handle_event(self, *args):
        event = args[0]
        player = args[2]
        enemies = args[3]

        player.handle_event(event, enemies)

        match event:
            case events.PlayerWon():
                return states.game.victory_screen_state.VictoryScreenState()
            case events.PlayerLost():
                return states.game.defeat_screen_state.DefeatScreenState()

    @property
    def sprite_group(self):
        return self.__sprite_group

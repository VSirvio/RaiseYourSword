from game import events
from game.enemy_spawner import EnemySpawner
import states.game.defeat_screen_state
import states.game.victory_screen_state

class PlayState:
    def __init__(self):
        self.__spawner = EnemySpawner()

    def draw(self, surface):
        pass

    def update(self, *args):
        dt = args[0]
        game = args[1]

        self.__spawner.spawn_enemies(dt, game)

    def handle_event(self, *args):
        event = args[0]
        player = args[1]
        enemies = args[2]

        player.handle_event(event, enemies)

        match event:
            case events.PlayerWon():
                return states.game.victory_screen_state.VictoryScreenState()
            case events.PlayerLost():
                return states.game.defeat_screen_state.DefeatScreenState()

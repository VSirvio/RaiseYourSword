import pygame

from game import events
from game.enemy_spawner import EnemySpawner
import states.game.defeat_screen_state
import states.game.victory_screen_state

class PlayState:
    """Game state for when the actual gameplay is on."""

    def __init__(self):
        self.__spawner = None
        self.__sprite_group = None

    def enter(self, game):
        """Called right after transitioning to this state.

        Args:
            game: The Game instance that this state belongs to.
        """

        self.__spawner = EnemySpawner(game)
        self.__sprite_group = pygame.sprite.Group()

    def update(self, *args):
        """Called once each game loop iteration.

        Args:
            dt: Time elapsed since the last game loop iteration in milliseconds.
            game: The Game instance that this state belongs to.
        """

        dt = args[0]
        game = args[1]

        self.__spawner.spawn_enemies(dt, game)

    def handle_event(self, *args):
        """Called when the game receives a game event.

        Args:
            event: Event object of one of the classes from the "events" module.
            player: The Character instance of the player character.
            enemies: List of the Character instances of the enemy characters.

        Returns:
            A new state that the game should now transition to or None.
        """

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
        """Sprite group related to the state to be rendered over game screen."""

        return self.__sprite_group

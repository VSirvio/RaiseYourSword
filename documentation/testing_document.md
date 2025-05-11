# Testing document

The testing of this game include automated unit and integration tests using the `unittest` package and manual system testing.

## Unit and integration testing

### Character class

Tests for [Character](https://github.com/VSirvio/RaiseYourSword/blob/main/src/game/character.py) class are located in the [tests/player_test.py](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/player_test.py) and [tests/enemy_test.py](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/enemy_test.py) files. In `tests/player_test.py` the `Character`  instance is initialized with same parameters as the player character in the game and in `tests/enemy_test.py` it is initialized like the enemy characters in the game. This makes it possible to test the class from both perspectives. Enemy tests require there to also be a player character or otherwise the enemy AI does not work correctly, so a `StubPlayer` class is provided in `tests/enemy_test.py` file.

### Configuration file

Existence of a valid game configuration file is required for all tests that use [GameConfig](https://github.com/VSirvio/RaiseYourSword/blob/main/src/configuration/game_config.py) class, so the configuration file is faked in these tests by creating a temporary file using `tempfile` package in Python's standard library.

### Utility classes and functions

Several of the game's utility classes and functions also have unit tests: [ArrowKeys](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/arrow_keys_test.py), [Direction](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/direction_test.py), [EnemySpawner](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/enemy_spawner_test.py), [load_config()](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/config_test.py) and [fill_with_tile()](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/utils_test.py).

### Integration testing of Game and GameLoop classes

The integration tests for the [Game](https://github.com/VSirvio/RaiseYourSword/blob/main/src/game/game.py) class can be found in the [tests/game_test.py](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/game_test.py) file and for the [GameLoop](https://github.com/VSirvio/RaiseYourSword/blob/main/src/game/game_loop.py) class in the [tests/game_loop_test.py](https://github.com/VSirvio/RaiseYourSword/blob/main/src/tests/game_loop_test.py) file.

The `GameLoop` instance is initialized in the tests by injecting stub classes into it replacing its actual dependencies: [Clock](https://github.com/VSirvio/RaiseYourSword/blob/main/src/services/clock.py), [EventQueue](https://github.com/VSirvio/RaiseYourSword/blob/main/src/services/event_queue.py), [Game](https://github.com/VSirvio/RaiseYourSword/blob/main/src/game/game.py) and [Renderer](https://github.com/VSirvio/RaiseYourSword/blob/main/src/services/renderer.py). This makes it possible to inject key presses to the `GameLoop` during the tests, disabling rendering graphics during the tests and making the game loop run any number of iterations instantly.

### States and components

AI, player and game states are tested as part of the tests of the `Character`, `Game` and `GameLoop` classes. They are inseparable part of the `Character` and `Game` classes and cannot function independently from these classes, so it is not meaningful to try to unit test them separately. Same holds for the component classes `AnimationsComponent`, `PhysicsComponent` and `PlayerPhysics`, as they are inseparable part of the functionality of the `Character` class.

### Data classes

Some classes are only meant for storing and organizing data and have no notable functionality of their own, so it is not meaningful to unit test them either. These classes include `AnimationSet`, `Animation`, `AttackAnimation`, `CharacterAnimation`, `AiConfig`, `GameConfig`, `GraphicsConfig`, `SpawningConfig`, `CharacterDirection` and `PlayerDirection`.

### Pygame interface abstractions

The pygame interface abstraction classes `Clock`, `EventQueue` and `Renderer` were not tested, because their only purpose is to provide an interface to certain pygame features and they do not include any functionality of their own.

### Testing coverage

The branch coverage of the tests is 88 %.

![](https://github.com/VSirvio/RaiseYourSword/blob/main/documentation/images/test_coverage.png)

Some notable things that could still be tested:
- Characters should not be able to walk through each other
- Enemies should be spawned outside the screen

## System testing

System testing for this game was performed manually.

### Installation and configuration

All installation, configuration and usage instructions in the [user manual](https://github.com/VSirvio/RaiseYourSword/tree/main/documentation/user_manual.md) were tried. Different values for the settings in the [game configuration file](https://github.com/VSirvio/RaiseYourSword/blob/main/src/config.yaml) were also tried.

### Functionality

All functionality listed in the [specification](https://github.com/VSirvio/RaiseYourSword/tree/main/documentation/specification.md) and the user manual was tested manually. Erroneous actions were also tried such as pressing keys that should not do anything.

## Quality issues remaining

A couple of things that came to light during playtesting by other people:
- Enemy idle animations are in sync with each other during the ending screen, which looks a bit silly.
- The visible effects of being hit by an attack seem to be slightly delayed compared to the attack animation.

# Changelog

## Week 2

- Added a player character with idle animation
- Added the capability to move the player character
- Added a sword attack for the player character
- Added the function `utils.fill_with_tile()` for filling the background with a repeating tile
- Tested that `utils.fill_with_tile()` fills the destination surface properly
- Added a simple grass texture to the background of the game
- Added a custom application icon to show in the application window title bar

## Week 3

- Added an enemy character with idle animation
- The player can defeat the enemy by attacking it and after that a screen with the text `You have won` is displayed
- Refactored the game loop into a separate `GameLoop` class
- Tested that the `Player.walk()` method moves the player character correctly
- Tested that the idle animation is played correctly when the player character is standing idle

## Week 4

- Added a sword attack for the enemy character
- Added to the enemy character the behavior that they repeat the sword attack endlessly
- The player can lose the game by being hit by the enemy's attack and after that a screen with the text `Game over` is displayed
- Tested that the attack animation is played correctly when the player character is attacking
- Tested that the player cannot move while attacking

## Week 5

- Refactored direction data structures into a separate `Direction` class
- Refactored directional key tracking into a separate `ArrowKeys` class
- Refactored graphics scaling factor to be only applied once, inside the `Renderer` class
- Refactored animations to use `State` design pattern
- Added an AI to the enemy that allows them to chase the player and try to attack them
- Tested that the enemy moves

## Week 6

- Refactored parts of `Player` and `Enemy` classes into smaller component classes `CharacterDirection`, `PlayerDirection`, `AnimationsComponent`, `PhysicsComponent` and `PlayerPhysics`
- Refactored `Player` and `Enemy` classes to be just one `Character` class
- Refactored the player state classes and AI state classes to have a single `handle_event()` method that can handle all different types of events instead of having a separate method for each type of event
- Changed the spawning behavior of enemies so that instead of there being just one enemy that is already there in the beginning of the game multiple enemies spawn off-screen at random times
- Added to the game logic the capability to precisely set on which attack animation frames does the attack hit the other character
- Added the capability to easily restart the game in the ending screen by pressing <kbd>Enter</kbd> or <kbd>Space</kbd>
- Tested that the current direction in the `ArrowKeys` class is `NONE` by default
- Tested that a key down event sets the current direction in the `ArrowKeys` class correctly
- Tested that all keys are released correctly in the `ArrowKeys` class, when the `release_all()` method is called

## Week 7

- Added support for game states (e.g. `VictoryScreenState` and `PlayState`)
- Added intro texts
- Added support for animation metadata YAML files
- Added death animations for the characters
- Added support for a game configuration file
- Fine-tuned hitboxes and bounding boxes
- Changed the enemy AI behavior so that enemies no longer walk through each other
- Changed the spawning behavior of enemies so that multiple enemies are spawned at the same time
- Updated the fonts used in the ending screen texts
- Added the feature that old enemy bodies vanish
- Added classes for storing game configuration to replace the use of global constants
- Tested `Game`, `GameLoop`, `EnemySpawner` and `Direction` classes and `load_config()` function

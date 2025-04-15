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

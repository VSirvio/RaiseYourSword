# Specification

## Purpose

The application is a 2D fantasy action game viewed from a top-down perspective. Its gameplay consists of fighting waves of monsters.

## Core functionality

- Player character:
  - Can move to four directions (up, down, left, right)
  - Can swing their sword, which will defeat any enemy in front of them with one hit
  - Has graphics:
    - Animations for moving to each direction and attacking to each direction
- Game area:
  - Is exactly of the size of the game window
  - Has a ground texture as a background
- Enemies:
  - Keep coming from outside the screen
  - Can move to four directions
  - Can attack, which will defeat the player with one hit, if the player is in front of them
  - Are controlled by the game:
    - Try to hit the player with their attacks
  - Have graphics:
    - Animations for moving to each direction and attacking to each direction
- Progression:
  - When the player has defeated all enemies in the wave, the player wins the game
  - The game can be quit by pressing Esc

## Extension ideas

- Losing the game takes more than one hit by the enemies (the player character should also have an animation to indicate they got hit)
- Defeating enemies takes multiple hits (they should also have an animation to indicate they got hit)
- HP display that shows the amount of HP the player has left
- A screen that shows the text "Victory", when the player wins the game
- A screen that shows the text "Game over", when the player loses the game
- Multiple waves of enemies with increasing length and number of enemies
- Different kinds of attacks for the player character to use (e.g. ranged attacks)
- Defeating enemies gives the player experience points (EXP) and gaining enough EXP unlocks new kinds of attacks
- Pause screen (where the player can also exit the game)
- Sound effects

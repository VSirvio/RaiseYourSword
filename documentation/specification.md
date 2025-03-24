
# Specification

## Purpose

The application is a 2D fantasy action game viewed from a top-down perspective. Its gameplay consists of fighting a horde of monsters emerging from off-screen.

## Core functionality

- Player character:
  - Can move to eight directions (up, right, down, left, and the diagonal directions between them)
  - Can swing their sword, which will defeat any enemy in front of them with one hit
  - Has graphics:
    - Animations for standing idle, walking and attacking (all animations have variations for each of the four main directions: up, down, left, right)
- Game area:
  - Is exactly of the size of the game window
  - Has a grass texture as a background
- Enemies:
  - Emerge from off-screen
  - Can move to eight directions
  - Can attack, which will defeat the player with one hit, if the player is in front of them (the text "Game over" appears on the screen, when the player is defeated)
  - Are controlled by the game:
    - Try to hit the player with their attacks
  - Have graphics:
    - Animations for standing idle, walking and attacking (all animations have variations for each of the four main directions)
  - When the player has defeated all the enemies in the horde, the player wins the game (the text "Victory" appears on the screen)

## Extension ideas

- Losing the game takes more than one hit by the enemies (the player character also has an animation to indicate they got hit)
- Defeating enemies takes multiple hits (they also have an animation to indicate they got hit)
- Hit points (HP) display that shows the amount of HP the player has left (HP decreases when the player gets hit by an enemy, and the player loses the game, when it reaches zero)
- Multiple waves of enemies with increasing length and number of enemies
- Different kinds of attacks for the player character to use (e.g. ranged attacks)
- Defeating enemies gives the player experience points (EXP) and gaining enough EXP unlocks new kinds of attacks
- Sound effects
